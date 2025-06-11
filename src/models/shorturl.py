from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import qrcode
from io import BytesIO
import base64
import os

db = SQLAlchemy()

class ShortURL(db.Model):
    __tablename__ = 'short_urls'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    custom_alias = db.Column(db.String(50), unique=True, nullable=True)
    domain = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    click_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('short_urls', lazy=True))
    analytics = db.relationship('URLAnalytics', backref='short_url', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, original_url, user_id=None, custom_alias=None, domain=None, expires_at=None):
        self.original_url = original_url
        self.user_id = user_id
        self.custom_alias = custom_alias
        self.domain = domain
        self.expires_at = expires_at
        
        if custom_alias:
            self.short_code = custom_alias
        else:
            self.short_code = self.generate_short_code()
    
    @staticmethod
    def generate_short_code(length=6):
        """Generate a random short code for the URL"""
        chars = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(chars) for _ in range(length))
            # Check if code already exists
            existing = ShortURL.query.filter_by(short_code=short_code).first()
            if not existing:
                return short_code
    
    def increment_click(self):
        """Increment the click count for this URL"""
        self.click_count += 1
        db.session.commit()
    
    def get_full_shortened_url(self):
        """Get the full shortened URL including domain"""
        if self.domain:
            return f"https://{self.domain}/{self.short_code}"
        else:
            # Use default domain if none specified
            return f"https://linkak.com/{self.short_code}"
    
    def generate_qr_code(self, size=200):
        """Generate a QR code for the shortened URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_full_shortened_url())
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def save_qr_code(self, path=None):
        """Save QR code to a file"""
        if not path:
            # Create directory if it doesn't exist
            os.makedirs('src/static/qrcodes', exist_ok=True)
            path = f"src/static/qrcodes/{self.short_code}.png"
            
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_full_shortened_url())
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path)
        return path
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'custom_alias': self.custom_alias,
            'domain': self.domain,
            'full_short_url': self.get_full_shortened_url(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'click_count': self.click_count,
            'is_active': self.is_active
        }


class URLAnalytics(db.Model):
    __tablename__ = 'url_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey('short_urls.id'), nullable=False)
    click_time = db.Column(db.DateTime, default=datetime.utcnow)
    referrer = db.Column(db.String(255), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 can be up to 45 chars
    country = db.Column(db.String(2), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(20), nullable=True)  # mobile, desktop, tablet
    browser = db.Column(db.String(50), nullable=True)
    os = db.Column(db.String(50), nullable=True)
    
    def __init__(self, short_url_id, referrer=None, user_agent=None, ip_address=None):
        self.short_url_id = short_url_id
        self.referrer = referrer
        self.user_agent = user_agent
        self.ip_address = ip_address
        
        # Parse user agent to get device, browser, OS info
        if user_agent:
            self.parse_user_agent(user_agent)
        
        # Get geolocation data if IP is provided
        if ip_address:
            self.get_geolocation(ip_address)
    
    def parse_user_agent(self, user_agent):
        """Parse user agent string to extract device, browser and OS info"""
        # This is a simplified version - in production you'd use a proper UA parser library
        ua_lower = user_agent.lower()
        
        # Detect device type
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            self.device_type = 'mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            self.device_type = 'tablet'
        else:
            self.device_type = 'desktop'
        
        # Detect browser
        if 'chrome' in ua_lower:
            self.browser = 'Chrome'
        elif 'firefox' in ua_lower:
            self.browser = 'Firefox'
        elif 'safari' in ua_lower:
            self.browser = 'Safari'
        elif 'edge' in ua_lower:
            self.browser = 'Edge'
        elif 'opera' in ua_lower:
            self.browser = 'Opera'
        else:
            self.browser = 'Other'
        
        # Detect OS
        if 'windows' in ua_lower:
            self.os = 'Windows'
        elif 'mac' in ua_lower:
            self.os = 'MacOS'
        elif 'linux' in ua_lower:
            self.os = 'Linux'
        elif 'android' in ua_lower:
            self.os = 'Android'
        elif 'ios' in ua_lower or 'iphone' in ua_lower or 'ipad' in ua_lower:
            self.os = 'iOS'
        else:
            self.os = 'Other'
    
    def get_geolocation(self, ip_address):
        """Get geolocation data from IP address"""
        # In a real implementation, you would use a geolocation API service
        # This is a placeholder - you'd replace with actual API call
        # Example services: MaxMind GeoIP, ipstack, ipinfo.io
        
        # For demo purposes, we'll just set placeholder values
        self.country = 'US'  # ISO country code
        self.city = 'New York'
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'short_url_id': self.short_url_id,
            'click_time': self.click_time.isoformat() if self.click_time else None,
            'referrer': self.referrer,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'country': self.country,
            'city': self.city,
            'device_type': self.device_type,
            'browser': self.browser,
            'os': self.os
        }
