"""
Security Middleware for Linkak
Implements comprehensive security measures for production deployment
"""

import os
import time
import hashlib
import logging
from functools import wraps
from flask import request, jsonify, current_app, g
from werkzeug.exceptions import TooManyRequests
from werkzeug.serving import WSGIRequestHandler
import redis
from typing import Dict, Any, Optional


logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Comprehensive security middleware for Linkak"""
    
    def __init__(self, app=None, redis_client=None):
        self.app = app
        self.redis_client = redis_client
        self.rate_limits = {}
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security middleware with Flask app"""
        self.app = app
        
        # Initialize Redis for rate limiting if not provided
        if not self.redis_client:
            redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/1')
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()  # Test connection
            except Exception as e:
                logger.warning(f"Redis not available for rate limiting: {e}")
                self.redis_client = None
        
        # Register middleware
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Security headers
        self.setup_security_headers(app)
        
        logger.info("Security middleware initialized")
    
    def setup_security_headers(self, app):
        """Setup security headers for all responses"""
        
        @app.after_request
        def add_security_headers(response):
            # Content Security Policy
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
                "https://www.google-analytics.com https://www.googletagmanager.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            )
            response.headers['Content-Security-Policy'] = csp
            
            # Other security headers
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # HSTS (only if using HTTPS)
            if request.is_secure:
                response.headers['Strict-Transport-Security'] = (
                    'max-age=31536000; includeSubDomains; preload'
                )
            
            # Remove server information
            response.headers.pop('Server', None)
            
            return response
    
    def get_client_identifier(self) -> str:
        """Get unique identifier for client (IP + User Agent hash)"""
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        
        # Create hash of IP + User Agent for privacy
        identifier = hashlib.sha256(f"{ip}:{user_agent}".encode()).hexdigest()[:16]
        return identifier
    
    def is_rate_limited(self, identifier: str, endpoint: str, limit: int, window: int) -> bool:
        """Check if client is rate limited"""
        if not self.redis_client:
            # Fallback to memory-based rate limiting (not recommended for production)
            return self._memory_rate_limit(identifier, endpoint, limit, window)
        
        try:
            key = f"rate_limit:{endpoint}:{identifier}"
            current_requests = self.redis_client.get(key)
            
            if current_requests is None:
                # First request in window
                self.redis_client.setex(key, window, 1)
                return False
            
            current_requests = int(current_requests)
            if current_requests >= limit:
                return True
            
            # Increment counter
            self.redis_client.incr(key)
            return False
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return False  # Allow request if rate limiting fails
    
    def _memory_rate_limit(self, identifier: str, endpoint: str, limit: int, window: int) -> bool:
        """Memory-based rate limiting (fallback)"""
        now = time.time()
        key = f"{endpoint}:{identifier}"
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Clean old requests
        self.rate_limits[key] = [
            req_time for req_time in self.rate_limits[key] 
            if now - req_time < window
        ]
        
        if len(self.rate_limits[key]) >= limit:
            return True
        
        self.rate_limits[key].append(now)
        return False
    
    def apply_rate_limiting(self):
        """Apply rate limiting based on endpoint"""
        identifier = self.get_client_identifier()
        endpoint = request.endpoint or 'unknown'
        
        # Define rate limits for different endpoints
        rate_limits = {
            'login': (5, 300),      # 5 attempts per 5 minutes
            'register': (3, 3600),   # 3 attempts per hour
            'api': (100, 3600),      # 100 requests per hour for API
            'default': (1000, 3600)  # 1000 requests per hour for general use
        }
        
        # Determine rate limit
        limit, window = rate_limits.get('default')
        
        if endpoint in ['user.login', 'login']:
            limit, window = rate_limits['login']
        elif endpoint in ['user.register', 'register']:
            limit, window = rate_limits['register']
        elif endpoint and endpoint.startswith('api.'):
            limit, window = rate_limits['api']
        
        # Check rate limit
        if self.is_rate_limited(identifier, endpoint, limit, window):
            logger.warning(f"Rate limit exceeded for {identifier} on {endpoint}")
            raise TooManyRequests(
                description="Rate limit exceeded. Please try again later."
            )
    
    def detect_suspicious_activity(self) -> Optional[str]:
        """Detect potentially suspicious requests"""
        # Check for common attack patterns
        suspicious_patterns = [
            'union select',
            'script>',
            '../',
            '<?php',
            'eval(',
            'base64_decode',
            'system(',
            'exec(',
            'passthru(',
            'shell_exec'
        ]
        
        # Check URL and parameters
        full_url = request.url.lower()
        for pattern in suspicious_patterns:
            if pattern in full_url:
                return f"Suspicious pattern in URL: {pattern}"
        
        # Check request body
        if request.data:
            try:
                body = request.data.decode('utf-8', errors='ignore').lower()
                for pattern in suspicious_patterns:
                    if pattern in body:
                        return f"Suspicious pattern in body: {pattern}"
            except:
                pass
        
        # Check headers for malicious content
        for header_name, header_value in request.headers:
            if header_value:
                header_lower = header_value.lower()
                for pattern in suspicious_patterns:
                    if pattern in header_lower:
                        return f"Suspicious pattern in {header_name} header: {pattern}"
        
        # Check for unusual request methods
        if request.method not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']:
            return f"Unusual HTTP method: {request.method}"
        
        return None
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events for monitoring"""
        log_entry = {
            'timestamp': time.time(),
            'event_type': event_type,
            'ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            'user_agent': request.headers.get('User-Agent', ''),
            'endpoint': request.endpoint,
            'method': request.method,
            'url': request.url,
            'details': details
        }
        
        # Log to file
        logger.warning(f"Security event: {event_type} - {details}")
        
        # Store in Redis for analysis if available
        if self.redis_client:
            try:
                key = f"security_events:{int(time.time())}"
                self.redis_client.setex(key, 86400, str(log_entry))  # Store for 24 hours
            except Exception as e:
                logger.error(f"Failed to store security event: {e}")
    
    def validate_file_upload(self, file) -> bool:
        """Validate file uploads for security"""
        if not file:
            return False
        
        # Check file size
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        if hasattr(file, 'content_length') and file.content_length > max_size:
            return False
        
        # Check file extension
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
        if '.' not in file.filename:
            return False
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return False
        
        # Check for malicious content in filename
        malicious_chars = ['..', '/', '\\', '<', '>', '|', ':', '*', '?', '"']
        for char in malicious_chars:
            if char in file.filename:
                return False
        
        return True
    
    def before_request(self):
        """Pre-request security checks"""
        try:
            # Skip security checks for health endpoint
            if request.endpoint == 'health_check':
                return
            
            # Apply rate limiting
            self.apply_rate_limiting()
            
            # Check for suspicious activity
            suspicious_activity = self.detect_suspicious_activity()
            if suspicious_activity:
                self.log_security_event('suspicious_request', {
                    'reason': suspicious_activity,
                    'blocked': True
                })
                return jsonify({'error': 'Request blocked for security reasons'}), 403
            
            # Validate Content-Type for POST requests
            if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type:
                allowed_content_types = [
                    'application/json',
                    'application/x-www-form-urlencoded',
                    'multipart/form-data',
                    'text/plain'
                ]
                
                content_type = request.content_type.split(';')[0]  # Remove charset
                if content_type not in allowed_content_types:
                    self.log_security_event('invalid_content_type', {
                        'content_type': content_type
                    })
                    return jsonify({'error': 'Invalid content type'}), 400
            
            # Store request start time for performance monitoring
            g.start_time = time.time()
            
        except TooManyRequests:
            raise  # Re-raise rate limiting exceptions
        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            # Don't block request on middleware errors
            return
    
    def after_request(self, response):
        """Post-request security actions"""
        try:
            # Log slow requests
            if hasattr(g, 'start_time'):
                duration = time.time() - g.start_time
                if duration > 5.0:  # Log requests taking more than 5 seconds
                    self.log_security_event('slow_request', {
                        'duration': duration,
                        'status_code': response.status_code
                    })
            
            # Log failed authentication attempts
            if response.status_code == 401:
                self.log_security_event('authentication_failure', {
                    'status_code': response.status_code
                })
            
            # Log other security-relevant status codes
            if response.status_code in [403, 429]:
                self.log_security_event('security_response', {
                    'status_code': response.status_code
                })
            
        except Exception as e:
            logger.error(f"After request security error: {e}")
        
        return response


def require_api_key(f):
    """Decorator to require API key for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = current_app.config.get('API_KEY')
        
        if not expected_key:
            # API key not configured, allow access
            return f(*args, **kwargs)
        
        if not api_key or api_key != expected_key:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def ip_whitelist_required(whitelist_env_var='IP_WHITELIST'):
    """Decorator to restrict access to whitelisted IPs"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            whitelist = os.environ.get(whitelist_env_var, '').split(',')
            whitelist = [ip.strip() for ip in whitelist if ip.strip()]
            
            if not whitelist:
                # No whitelist configured, allow access
                return f(*args, **kwargs)
            
            client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            
            if client_ip not in whitelist:
                logger.warning(f"Access denied for IP {client_ip}, not in whitelist")
                return jsonify({'error': 'Access denied'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator