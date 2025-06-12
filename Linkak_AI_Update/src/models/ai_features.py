from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from src.models.user import db, User, Link

class SmartLinkCategorization(db.Model):
    """AI-powered automatic link categorization system"""
    __tablename__ = 'smart_link_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    suggested_category = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    is_applied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('smart_categories', lazy=True))
    link = db.relationship('Link', backref=db.backref('smart_categories', lazy=True))
    
    def __init__(self, user_id, link_id, suggested_category, confidence_score):
        self.user_id = user_id
        self.link_id = link_id
        self.suggested_category = suggested_category
        self.confidence_score = confidence_score
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link_id': self.link_id,
            'suggested_category': self.suggested_category,
            'confidence_score': self.confidence_score,
            'is_applied': self.is_applied,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LinkHealthMonitor(db.Model):
    """AI-powered link health monitoring system"""
    __tablename__ = 'link_health_monitors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)  # 'healthy', 'broken', 'redirected', 'slow', 'warning'
    response_time = db.Column(db.Float, nullable=True)  # in seconds
    status_code = db.Column(db.Integer, nullable=True)
    redirect_url = db.Column(db.String(2048), nullable=True)
    issues = db.Column(db.Text, nullable=True)  # JSON string of detected issues
    
    # Relationships
    user = db.relationship('User', backref=db.backref('link_health_monitors', lazy=True))
    link = db.relationship('Link', backref=db.backref('health_monitor', lazy=True))
    
    def __init__(self, user_id, link_id, status, response_time=None, status_code=None, redirect_url=None):
        self.user_id = user_id
        self.link_id = link_id
        self.status = status
        self.response_time = response_time
        self.status_code = status_code
        self.redirect_url = redirect_url
    
    def get_issues(self):
        """Get issues as a list"""
        if self.issues:
            try:
                return json.loads(self.issues)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_issues(self, issues_list):
        """Set issues from a list"""
        if isinstance(issues_list, list):
            self.issues = json.dumps(issues_list)
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link_id': self.link_id,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'status': self.status,
            'response_time': self.response_time,
            'status_code': self.status_code,
            'redirect_url': self.redirect_url,
            'issues': self.get_issues()
        }


class SecurityScan(db.Model):
    """AI-powered link security scanning system"""
    __tablename__ = 'security_scans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    security_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    risk_level = db.Column(db.String(50), nullable=False)  # 'safe', 'low_risk', 'medium_risk', 'high_risk', 'dangerous'
    threats_detected = db.Column(db.Text, nullable=True)  # JSON string of detected threats
    
    # Relationships
    user = db.relationship('User', backref=db.backref('security_scans', lazy=True))
    link = db.relationship('Link', backref=db.backref('security_scans', lazy=True))
    
    def __init__(self, user_id, link_id, security_score, risk_level):
        self.user_id = user_id
        self.link_id = link_id
        self.security_score = security_score
        self.risk_level = risk_level
    
    def get_threats(self):
        """Get threats as a list of dictionaries"""
        if self.threats_detected:
            try:
                return json.loads(self.threats_detected)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_threats(self, threats_list):
        """Set threats from a list of dictionaries"""
        if isinstance(threats_list, list):
            self.threats_detected = json.dumps(threats_list)
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link_id': self.link_id,
            'scan_date': self.scan_date.isoformat() if self.scan_date else None,
            'security_score': self.security_score,
            'risk_level': self.risk_level,
            'threats_detected': self.get_threats()
        }


class ContentInsight(db.Model):
    """AI-powered content analysis and insights"""
    __tablename__ = 'content_insights'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.Text, nullable=True)  # JSON string of keywords
    summary = db.Column(db.Text, nullable=True)
    content_type = db.Column(db.String(50), nullable=True)  # 'article', 'product', 'video', etc.
    sentiment_score = db.Column(db.Float, nullable=True)  # -1.0 to 1.0
    reading_time = db.Column(db.Integer, nullable=True)  # in seconds
    
    # Relationships
    user = db.relationship('User', backref=db.backref('content_insights', lazy=True))
    link = db.relationship('Link', backref=db.backref('content_insight', lazy=True))
    
    def __init__(self, user_id, link_id, title=None, description=None, content_type=None):
        self.user_id = user_id
        self.link_id = link_id
        self.title = title
        self.description = description
        self.content_type = content_type
    
    def get_keywords(self):
        """Get keywords as a list"""
        if self.keywords:
            try:
                return json.loads(self.keywords)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_keywords(self, keywords_list):
        """Set keywords from a list"""
        if isinstance(keywords_list, list):
            self.keywords = json.dumps(keywords_list)
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link_id': self.link_id,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'title': self.title,
            'description': self.description,
            'keywords': self.get_keywords(),
            'summary': self.summary,
            'content_type': self.content_type,
            'sentiment_score': self.sentiment_score,
            'reading_time': self.reading_time
        }


class AudienceMatch(db.Model):
    """AI-powered audience matching and targeting"""
    __tablename__ = 'audience_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    audience_segments = db.Column(db.Text, nullable=True)  # JSON string of audience segments
    best_platforms = db.Column(db.Text, nullable=True)  # JSON string of recommended platforms
    optimal_times = db.Column(db.Text, nullable=True)  # JSON string of optimal posting times
    
    # Relationships
    user = db.relationship('User', backref=db.backref('audience_matches', lazy=True))
    link = db.relationship('Link', backref=db.backref('audience_match', lazy=True))
    
    def __init__(self, user_id, link_id):
        self.user_id = user_id
        self.link_id = link_id
    
    def get_audience_segments(self):
        """Get audience segments as a dictionary"""
        if self.audience_segments:
            try:
                return json.loads(self.audience_segments)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_audience_segments(self, segments_dict):
        """Set audience segments from a dictionary"""
        if isinstance(segments_dict, dict):
            self.audience_segments = json.dumps(segments_dict)
    
    def get_best_platforms(self):
        """Get best platforms as a list of dictionaries"""
        if self.best_platforms:
            try:
                return json.loads(self.best_platforms)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_best_platforms(self, platforms_list):
        """Set best platforms from a list of dictionaries"""
        if isinstance(platforms_list, list):
            self.best_platforms = json.dumps(platforms_list)
    
    def get_optimal_times(self):
        """Get optimal times as a dictionary"""
        if self.optimal_times:
            try:
                return json.loads(self.optimal_times)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_optimal_times(self, times_dict):
        """Set optimal times from a dictionary"""
        if isinstance(times_dict, dict):
            self.optimal_times = json.dumps(times_dict)
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link_id': self.link_id,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'audience_segments': self.get_audience_segments(),
            'best_platforms': self.get_best_platforms(),
            'optimal_times': self.get_optimal_times()
        }


class SmartLinkPreview(db.Model):
    """AI-generated enhanced link previews"""
    __tablename__ = 'smart_link_previews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(2048), nullable=True)
    favicon_url = db.Column(db.String(2048), nullable=True)
    preview_type = db.Column(db.String(50), default='standard')  # 'standard', 'enhanced', 'custom'
    custom_data = db.Column(db.Text, nullable=True)  # JSON string of custom preview data
    
    # Relationships
    user = db.relationship('User', backref=db.backref('smart_previews', lazy=True))
    link = db.relationship('Link', backref=db.backref('smart_preview', lazy=True))
    
    def __init__(self, user_id, link_id, title=None, description=None, image_url=None, preview_type='standard'):
        self.user_id = user_id
        self.link_id = link_id
        self.title = title
        self.description = description
        self.image_url = image_url
        self.preview_type = preview_type
    
    def get_custom_data(self):
        """Get custom data as a dictionary"""
        if self.custom_data:
            try:
                return json.loads(self.custom_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_custom_data(self, data_dict):
        """Set custom data from a dictionary"""
        if isinstance(data_dict, dict):
            self.custom_data = json.dumps(data_dict)
    
    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'link_id': self.link_id,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'favicon_url': self.favicon_url,
            'preview_type': self.preview_type,
            'custom_data': self.get_custom_data()
        }
