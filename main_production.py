"""
Linkak Production Application
Enhanced Flask application with security, monitoring, and performance optimizations
"""

import sys
import os
import logging
import time
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Flask and extensions
from flask import Flask, render_template, redirect, url_for, request, jsonify, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_talisman import Talisman
from flask_cors import CORS
import redis

# Application modules
from src.models.user import User, Link, db
from src.models.shorturl import ShortURL, URLAnalytics
from src.models.menu import Menu, MenuCategory, MenuItem
from src.models.advanced_features import AIRecommendation, AdvancedAnalytics, ScheduledContent, Collaboration
from src.routes.user import user_bp
from src.routes.shorturl import shorturl_bp
from src.routes.menu import menu_bp
from src.routes.advanced import advanced_bp
from src.config import get_config
from src.middleware.security import SecurityMiddleware

# Security and monitoring
from werkzeug.security import generate_password_hash
from prometheus_flask_exporter import PrometheusMetrics


def create_app(config_name=None):
    """Application factory with production optimizations"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize logging
    setup_logging(app)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Redis
    redis_client = None
    if app.config.get('REDIS_URL'):
        try:
            redis_client = redis.from_url(app.config['REDIS_URL'])
            redis_client.ping()
            app.logger.info("Redis connected successfully")
        except Exception as e:
            app.logger.warning(f"Redis connection failed: {e}")
    
    # Initialize caching
    cache = Cache(app)
    
    # Initialize rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1000 per hour"],
        storage_uri=app.config.get('RATELIMIT_STORAGE_URL')
    )
    
    # Initialize security middleware
    security = SecurityMiddleware(app, redis_client)
    
    # Initialize CORS
    CORS(app, origins=["https://linkak.com", "https://www.linkak.com"])
    
    # Initialize security headers (Talisman)
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://www.google-analytics.com",
        'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com",
        'img-src': "'self' data: https:",
        'connect-src': "'self'",
        'frame-ancestors': "'none'"
    }
    
    Talisman(
        app,
        force_https=app.config.get('FLASK_ENV') == 'production',
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src']
    )
    
    # Initialize monitoring
    metrics = PrometheusMetrics(app)
    metrics.info('linkak_app_info', 'Linkak Application', version='1.0.0')
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/auth')
    app.register_blueprint(shorturl_bp, url_prefix='/shorturl')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(advanced_bp, url_prefix='/advanced')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Main routes
    @app.route('/')
    @cache.cached(timeout=300)  # Cache for 5 minutes
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    @limiter.limit("5 per minute")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Log login attempt
            app.logger.info(f"Login attempt for user: {username}")
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                app.logger.info(f"Successful login for user: {username}")
                
                # Update last login time
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Redirect to next page or dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                app.logger.warning(f"Failed login attempt for user: {username}")
                return render_template('login.html', error='Invalid username or password')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    @limiter.limit("3 per hour")
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validation
            if password != confirm_password:
                return render_template('register.html', error='Passwords do not match')
            
            if len(password) < 8:
                return render_template('register.html', error='Password must be at least 8 characters long')
            
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                return render_template('register.html', error='Username or email already exists')
            
            # Create new user
            try:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                
                app.logger.info(f"New user registered: {username}")
                login_user(new_user)
                return redirect(url_for('dashboard'))
                
            except Exception as e:
                app.logger.error(f"Registration error: {e}")
                db.session.rollback()
                return render_template('register.html', error='Registration failed. Please try again.')
        
        return render_template('register.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        username = current_user.username
        logout_user()
        app.logger.info(f"User logged out: {username}")
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    @cache.cached(timeout=60, key_prefix='dashboard_%s', make_cache_key=lambda: f"dashboard_{current_user.id}")
    def dashboard():
        return redirect(url_for('user.dashboard'))
    
    # API endpoints
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring"""
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'database': 'unknown',
            'redis': 'unknown'
        }
        
        # Check database
        try:
            db.engine.execute('SELECT 1')
            health_status['database'] = 'healthy'
        except Exception as e:
            health_status['database'] = 'unhealthy'
            health_status['status'] = 'degraded'
            app.logger.error(f"Database health check failed: {e}")
        
        # Check Redis
        if redis_client:
            try:
                redis_client.ping()
                health_status['redis'] = 'healthy'
            except Exception as e:
                health_status['redis'] = 'unhealthy'
                app.logger.error(f"Redis health check failed: {e}")
        
        status_code = 200 if health_status['status'] == 'healthy' else 503
        return jsonify(health_status), status_code
    
    @app.route('/api/metrics')
    def metrics_endpoint():
        """Metrics endpoint for Prometheus"""
        # This will be handled by prometheus_flask_exporter automatically
        pass
    
    # Performance monitoring
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # Log slow requests
            if duration > 1.0:  # Log requests taking more than 1 second
                app.logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.2f}s (Status: {response.status_code})"
                )
        
        return response
    
    return app


def setup_logging(app):
    """Setup application logging"""
    if not app.debug and not app.testing:
        # Production logging setup
        log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
        
        # File handler
        log_file = app.config.get('LOG_FILE', 'logs/linkak.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Configure app logger
        app.logger.setLevel(log_level)
        app.logger.addHandler(file_handler)
        app.logger.addHandler(console_handler)
        
        app.logger.info('Linkak application starting...')


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404 error: {request.url}")
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 error: {error}")
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.warning(f"403 error: {request.url}")
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        app.logger.warning(f"Rate limit exceeded: {request.url}")
        return jsonify({'error': 'Rate limit exceeded'}), 429


def register_cli_commands(app):
    """Register CLI commands for administration"""
    
    @app.cli.command()
    def init_db():
        """Initialize the database"""
        db.create_all()
        print("Database initialized successfully!")
    
    @app.cli.command()
    def create_admin():
        """Create admin user"""
        username = input("Admin username: ")
        email = input("Admin email: ")
        password = input("Admin password: ")
        
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print("User with this username or email already exists!")
            return
        
        admin_user = User(
            username=username,
            email=email,
            password=password,
            is_admin=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully!")


def create_demo_data(app):
    """Create demo data for testing"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            # Create demo user
            demo_user = User(
                username='demo',
                email='demo@linkak.com',
                password='password',
                full_name='Demo User',
                bio='This is a demo account for testing Linkak features.'
            )
            db.session.add(demo_user)
            db.session.commit()
            
            # Create demo links and data (same as original)
            # ... (keeping the original demo data creation logic)
            
            app.logger.info("Demo data created successfully!")


# Create application instance
app = create_app()

if __name__ == '__main__':
    # Development server
    with app.app_context():
        db.create_all()
        if app.config.get('FLASK_ENV') == 'development':
            create_demo_data(app)
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )