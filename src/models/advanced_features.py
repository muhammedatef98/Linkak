from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class AIRecommendation(db.Model):
    __tablename__ = 'ai_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'layout', 'content', 'theme', etc.
    recommendation_data = db.Column(db.Text, nullable=False)  # JSON string of recommendation data
    is_applied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('ai_recommendations', lazy=True))
    
    def __init__(self, user_id, recommendation_type, recommendation_data):
        self.user_id = user_id
        self.recommendation_type = recommendation_type
        self.set_recommendation_data(recommendation_data)
    
    def get_recommendation_data(self):
        """Get recommendation data as a dictionary"""
        try:
            return json.loads(self.recommendation_data)
        except json.JSONDecodeError:
            return {}
    
    def set_recommendation_data(self, data_dict):
        """Set recommendation data from a dictionary"""
        if isinstance(data_dict, dict):
            self.recommendation_data = json.dumps(data_dict)
        else:
            self.recommendation_data = json.dumps({})
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_type': self.recommendation_type,
            'recommendation_data': self.get_recommendation_data(),
            'is_applied': self.is_applied,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AdvancedAnalytics(db.Model):
    __tablename__ = 'advanced_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_views = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    bounce_rate = db.Column(db.Float, nullable=True)
    avg_time_on_page = db.Column(db.Float, nullable=True)  # in seconds
    device_data = db.Column(db.Text, nullable=True)  # JSON string of device breakdown
    location_data = db.Column(db.Text, nullable=True)  # JSON string of location breakdown
    referrer_data = db.Column(db.Text, nullable=True)  # JSON string of referrer breakdown
    conversion_data = db.Column(db.Text, nullable=True)  # JSON string of conversion data
    
    # Relationships
    user = db.relationship('User', backref=db.backref('analytics', lazy=True))
    
    def __init__(self, user_id, date, total_views=0, unique_visitors=0):
        self.user_id = user_id
        self.date = date
        self.total_views = total_views
        self.unique_visitors = unique_visitors
    
    def get_device_data(self):
        """Get device data as a dictionary"""
        if self.device_data:
            try:
                return json.loads(self.device_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_device_data(self, data_dict):
        """Set device data from a dictionary"""
        if isinstance(data_dict, dict):
            self.device_data = json.dumps(data_dict)
    
    def get_location_data(self):
        """Get location data as a dictionary"""
        if self.location_data:
            try:
                return json.loads(self.location_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_location_data(self, data_dict):
        """Set location data from a dictionary"""
        if isinstance(data_dict, dict):
            self.location_data = json.dumps(data_dict)
    
    def get_referrer_data(self):
        """Get referrer data as a dictionary"""
        if self.referrer_data:
            try:
                return json.loads(self.referrer_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_referrer_data(self, data_dict):
        """Set referrer data from a dictionary"""
        if isinstance(data_dict, dict):
            self.referrer_data = json.dumps(data_dict)
    
    def get_conversion_data(self):
        """Get conversion data as a dictionary"""
        if self.conversion_data:
            try:
                return json.loads(self.conversion_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_conversion_data(self, data_dict):
        """Set conversion data from a dictionary"""
        if isinstance(data_dict, dict):
            self.conversion_data = json.dumps(data_dict)
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'total_views': self.total_views,
            'unique_visitors': self.unique_visitors,
            'bounce_rate': self.bounce_rate,
            'avg_time_on_page': self.avg_time_on_page,
            'device_data': self.get_device_data(),
            'location_data': self.get_location_data(),
            'referrer_data': self.get_referrer_data(),
            'conversion_data': self.get_conversion_data()
        }


class ScheduledContent(db.Model):
    __tablename__ = 'scheduled_content'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'link', 'theme', 'profile', etc.
    content_id = db.Column(db.Integer, nullable=True)  # ID of the content to modify
    action = db.Column(db.String(50), nullable=False)  # 'activate', 'deactivate', 'update', etc.
    scheduled_time = db.Column(db.DateTime, nullable=False)
    is_executed = db.Column(db.Boolean, default=False)
    execution_time = db.Column(db.DateTime, nullable=True)
    content_data = db.Column(db.Text, nullable=True)  # JSON string of content data for updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('scheduled_content', lazy=True))
    
    def __init__(self, user_id, content_type, action, scheduled_time, content_id=None, content_data=None):
        self.user_id = user_id
        self.content_type = content_type
        self.action = action
        self.scheduled_time = scheduled_time
        self.content_id = content_id
        
        if content_data and isinstance(content_data, dict):
            self.content_data = json.dumps(content_data)
    
    def get_content_data(self):
        """Get content data as a dictionary"""
        if self.content_data:
            try:
                return json.loads(self.content_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_content_data(self, data_dict):
        """Set content data from a dictionary"""
        if isinstance(data_dict, dict):
            self.content_data = json.dumps(data_dict)
    
    def mark_executed(self):
        """Mark this scheduled content as executed"""
        self.is_executed = True
        self.execution_time = datetime.utcnow()
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_type': self.content_type,
            'content_id': self.content_id,
            'action': self.action,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'is_executed': self.is_executed,
            'execution_time': self.execution_time.isoformat() if self.execution_time else None,
            'content_data': self.get_content_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Collaboration(db.Model):
    __tablename__ = 'collaborations'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    collaborator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # 'profile', 'menu', etc.
    resource_id = db.Column(db.Integer, nullable=False)
    permission_level = db.Column(db.String(50), nullable=False)  # 'view', 'edit', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id], backref=db.backref('owned_collaborations', lazy=True))
    collaborator = db.relationship('User', foreign_keys=[collaborator_id], backref=db.backref('collaborations', lazy=True))
    
    def __init__(self, owner_id, collaborator_id, resource_type, resource_id, permission_level):
        self.owner_id = owner_id
        self.collaborator_id = collaborator_id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.permission_level = permission_level
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'collaborator_id': self.collaborator_id,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'permission_level': self.permission_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
