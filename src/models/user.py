from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile settings
    theme = db.Column(db.String(50), default='default')
    social_links = db.Column(db.Text, nullable=True)  # JSON string of social links
    custom_domain = db.Column(db.String(255), nullable=True)
    profile_settings = db.Column(db.Text, nullable=True)  # JSON string of profile settings
    
    # Relationships
    links = db.relationship('Link', backref='user', lazy=True, cascade="all, delete-orphan")
    # Other relationships are defined in their respective models
    
    def __init__(self, username, email, password, full_name=None, bio=None, profile_image=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.full_name = full_name
        self.bio = bio
        self.profile_image = profile_image
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_social_links(self):
        """Get social links as a dictionary"""
        if self.social_links:
            try:
                return json.loads(self.social_links)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_social_links(self, links_dict):
        """Set social links from a dictionary"""
        if isinstance(links_dict, dict):
            self.social_links = json.dumps(links_dict)
    
    def get_profile_settings(self):
        """Get profile settings as a dictionary"""
        if self.profile_settings:
            try:
                return json.loads(self.profile_settings)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_profile_settings(self, settings_dict):
        """Set profile settings from a dictionary"""
        if isinstance(settings_dict, dict):
            self.profile_settings = json.dumps(settings_dict)
    
    def to_dict(self, include_private=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'profile_image': self.profile_image,
            'theme': self.theme,
            'social_links': self.get_social_links(),
            'custom_domain': self.custom_domain,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_private:
            data.update({
                'email': self.email,
                'is_active': self.is_active,
                'is_admin': self.is_admin,
                'profile_settings': self.get_profile_settings(),
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            })
        
        return data


class Link(db.Model):
    __tablename__ = 'links'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)  # Font Awesome icon class
    custom_image = db.Column(db.String(255), nullable=True)  # Path to custom image
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    click_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Link type (standard, menu, shorturl, etc.)
    link_type = db.Column(db.String(20), default='standard')
    
    # Reference to other entities based on link_type
    reference_id = db.Column(db.Integer, nullable=True)  # ID of the referenced entity
    
    # Additional settings
    settings = db.Column(db.Text, nullable=True)  # JSON string of link settings
    
    def __init__(self, title, url, user_id, description=None, icon=None, custom_image=None, 
                 category=None, is_featured=False, display_order=0, link_type='standard', reference_id=None):
        self.title = title
        self.url = url
        self.user_id = user_id
        self.description = description
        self.icon = icon
        self.custom_image = custom_image
        self.category = category
        self.is_featured = is_featured
        self.display_order = display_order
        self.link_type = link_type
        self.reference_id = reference_id
    
    def increment_click(self):
        """Increment the click count for this link"""
        self.click_count += 1
        db.session.commit()
    
    def get_settings(self):
        """Get settings as a dictionary"""
        if self.settings:
            try:
                return json.loads(self.settings)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_settings(self, settings_dict):
        """Set settings from a dictionary"""
        if isinstance(settings_dict, dict):
            self.settings = json.dumps(settings_dict)
    
    def to_dict(self):
        """Convert link to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'icon': self.icon,
            'custom_image': self.custom_image,
            'category': self.category,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'display_order': self.display_order,
            'click_count': self.click_count,
            'link_type': self.link_type,
            'reference_id': self.reference_id,
            'settings': self.get_settings(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
