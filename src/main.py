import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from src.models.user import User, Link, db
from src.models.shorturl import ShortURL, URLAnalytics
from src.models.menu import Menu, MenuCategory, MenuItem
from src.models.advanced_features import AIRecommendation, AdvancedAnalytics, ScheduledContent, Collaboration
from src.routes.user import user_bp
from src.routes.shorturl import shorturl_bp
from src.routes.menu import menu_bp
from src.routes.advanced import advanced_bp
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linkak.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(shorturl_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(advanced_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return render_template('register.html', error='Username or email already exists')
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('user.dashboard'))

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok', 'version': '1.0.0'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

def create_demo_data():
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
            
            # Create some links
            links = [
                Link(
                    title='My Website',
                    url='https://example.com',
                    user_id=demo_user.id,
                    icon='globe',
                    category='Personal',
                    is_featured=True,
                    display_order=1
                ),
                Link(
                    title='GitHub',
                    url='https://github.com',
                    user_id=demo_user.id,
                    icon='github',
                    category='Professional',
                    display_order=2
                ),
                Link(
                    title='Twitter',
                    url='https://twitter.com',
                    user_id=demo_user.id,
                    icon='twitter',
                    category='Social',
                    display_order=3
                ),
                Link(
                    title='LinkedIn',
                    url='https://linkedin.com',
                    user_id=demo_user.id,
                    icon='linkedin',
                    category='Professional',
                    is_featured=True,
                    display_order=4
                )
            ]
            
            for link in links:
                db.session.add(link)
            
            # Create a short URL
            short_url = ShortURL(
                original_url='https://example.com/very/long/url/that/needs/shortening',
                user_id=demo_user.id,
                custom_alias='demo'
            )
            db.session.add(short_url)
            
            # Create a menu
            menu = Menu(
                name='My Restaurant Menu',
                user_id=demo_user.id,
                business_name='Demo Restaurant',
                description='Delicious food for everyone',
                theme='restaurant'
            )
            db.session.add(menu)
            db.session.commit()
            
            # Create menu categories
            categories = [
                MenuCategory(
                    name='Appetizers',
                    menu_id=menu.id,
                    description='Start your meal right',
                    display_order=1
                ),
                MenuCategory(
                    name='Main Courses',
                    menu_id=menu.id,
                    description='Hearty and delicious',
                    display_order=2
                ),
                MenuCategory(
                    name='Desserts',
                    menu_id=menu.id,
                    description='Sweet treats',
                    display_order=3
                )
            ]
            
            for category in categories:
                db.session.add(category)
            db.session.commit()
            
            # Create menu items
            items = [
                MenuItem(
                    name='Mozzarella Sticks',
                    category_id=categories[0].id,
                    description='Crispy outside, gooey inside',
                    price=8.99,
                    is_featured=True,
                    display_order=1
                ),
                MenuItem(
                    name='Chicken Wings',
                    category_id=categories[0].id,
                    description='Spicy and tangy',
                    price=10.99,
                    display_order=2
                ),
                MenuItem(
                    name='Steak',
                    category_id=categories[1].id,
                    description='Juicy and tender',
                    price=24.99,
                    is_featured=True,
                    display_order=1
                ),
                MenuItem(
                    name='Pasta Carbonara',
                    category_id=categories[1].id,
                    description='Creamy and rich',
                    price=16.99,
                    display_order=2
                ),
                MenuItem(
                    name='Chocolate Cake',
                    category_id=categories[2].id,
                    description='Decadent and moist',
                    price=7.99,
                    is_featured=True,
                    display_order=1
                ),
                MenuItem(
                    name='Ice Cream',
                    category_id=categories[2].id,
                    description='Variety of flavors',
                    price=5.99,
                    display_order=2
                )
            ]
            
            for item in items:
                db.session.add(item)
            
            # Add menu link to profile
            menu_link = Link(
                title='My Restaurant Menu',
                url=menu.get_full_url(),
                user_id=demo_user.id,
                icon='utensils',
                category='Business',
                is_featured=True,
                display_order=5,
                link_type='menu',
                reference_id=menu.id
            )
            db.session.add(menu_link)
            
            # Add short URL link to profile
            shorturl_link = Link(
                title='My Short URL',
                url=short_url.get_full_shortened_url(),
                user_id=demo_user.id,
                icon='link',
                category='Tools',
                display_order=6,
                link_type='shorturl',
                reference_id=short_url.id
            )
            db.session.add(shorturl_link)
            
            # Create some AI recommendations
            recommendations = [
                AIRecommendation(
                    user_id=demo_user.id,
                    recommendation_type='layout',
                    recommendation_data={
                        'suggestion': 'Optimize your profile layout for better engagement',
                        'changes': [
                            {'type': 'move', 'item': 'featured_links', 'position': 'top'},
                            {'type': 'group', 'items': ['social_media_links'], 'label': 'Connect With Me'}
                        ],
                        'reasoning': 'Based on visitor behavior, featuring your most important links at the top can increase click-through rates by 30%.'
                    }
                ),
                AIRecommendation(
                    user_id=demo_user.id,
                    recommendation_type='content',
                    recommendation_data={
                        'suggestion': 'Add missing content types to increase engagement',
                        'changes': [
                            {'type': 'add', 'content_type': 'video', 'label': 'Watch My Latest Video'},
                            {'type': 'add', 'content_type': 'newsletter', 'label': 'Subscribe to Updates'}
                        ],
                        'reasoning': 'Profiles with multimedia content see 45% higher engagement rates.'
                    }
                )
            ]
            
            for rec in recommendations:
                db.session.add(rec)
            
            # Create scheduled content
            tomorrow = datetime.utcnow() + timedelta(days=1)
            scheduled = ScheduledContent(
                user_id=demo_user.id,
                content_type='link',
                action='activate',
                scheduled_time=tomorrow,
                content_id=1,
                content_data={'is_active': True}
            )
            db.session.add(scheduled)
            
            db.session.commit()
            print("Demo data created successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_demo_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
