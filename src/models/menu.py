from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    business_logo = db.Column(db.String(255), nullable=True)  # Path to logo image
    theme = db.Column(db.String(50), default='default')
    is_published = db.Column(db.Boolean, default=False)
    custom_url = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('menus', lazy=True))
    categories = db.relationship('MenuCategory', backref='menu', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, user_id, business_name, description=None, business_logo=None, theme='default', custom_url=None):
        self.name = name
        self.user_id = user_id
        self.business_name = business_name
        self.description = description
        self.business_logo = business_logo
        self.theme = theme
        self.custom_url = custom_url
    
    def to_dict(self):
        """Convert menu to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'business_name': self.business_name,
            'business_logo': self.business_logo,
            'theme': self.theme,
            'is_published': self.is_published,
            'custom_url': self.custom_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'categories': [category.to_dict() for category in self.categories]
        }
    
    def get_full_url(self):
        """Get the full URL for this menu"""
        if self.custom_url:
            return f"https://linkak.com/menu/{self.custom_url}"
        else:
            return f"https://linkak.com/menu/{self.id}"


class MenuCategory(db.Model):
    __tablename__ = 'menu_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('MenuItem', backref='category', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, menu_id, description=None, display_order=0):
        self.name = name
        self.menu_id = menu_id
        self.description = description
        self.display_order = display_order
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(255), nullable=True)  # Path to item image
    category_id = db.Column(db.Integer, db.ForeignKey('menu_categories.id'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    options = db.Column(db.Text, nullable=True)  # JSON string of options
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, category_id, description=None, price=None, image=None, 
                 is_available=True, is_featured=False, display_order=0, options=None):
        self.name = name
        self.category_id = category_id
        self.description = description
        self.price = price
        self.image = image
        self.is_available = is_available
        self.is_featured = is_featured
        self.display_order = display_order
        
        # Convert options dict to JSON string if provided
        if options and isinstance(options, dict):
            self.options = json.dumps(options)
        else:
            self.options = options
    
    def get_options(self):
        """Get options as a dictionary"""
        if self.options:
            try:
                return json.loads(self.options)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def to_dict(self):
        """Convert item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'display_order': self.display_order,
            'options': self.get_options(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
