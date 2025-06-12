import os
import sys
import json
import unittest
sys.path.append('/home/ubuntu/Linkak')

from flask import Flask
from src.models.ai_features import (
    db, SmartLinkCategorization, LinkHealthMonitor, SecurityScan, 
    ContentInsight, AudienceMatch, SmartLinkPreview
)
from src.models.user import User, Link
from src.routes.ai_features import ai_features_bp

class TestAIFeatures(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = Flask(__name__)
        
        # Configure the app for testing
        instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        db_path = os.path.join(instance_path, 'linkak.db')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_key'
        
        # Register the AI features blueprint
        self.app.register_blueprint(ai_features_bp)
        
        # Initialize the database
        db.init_app(self.app)
        
        # Create a test client
        self.client = self.app.test_client()
        
        # Create application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Ensure we have test data
        self.create_test_data()
    
    def tearDown(self):
        # Clean up after the test
        self.app_context.pop()
    
    def create_test_data(self):
        """Create test user and links for testing"""
        # Check if test user already exists
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            # Create a test user - using correct parameters from User model
            test_user = User(
                username='testuser',
                email='test@example.com',
                password='password',
                full_name='Test User'
            )
            db.session.add(test_user)
            db.session.commit()
        
        # Check if test links already exist
        test_links = Link.query.filter_by(user_id=test_user.id).all()
        if not test_links:
            # Create some test links
            links = [
                Link(
                    user_id=test_user.id,
                    title='GitHub',
                    url='https://github.com',
                    description='Code hosting platform'
                ),
                Link(
                    user_id=test_user.id,
                    title='LinkedIn',
                    url='https://linkedin.com',
                    description='Professional networking'
                ),
                Link(
                    user_id=test_user.id,
                    title='YouTube',
                    url='https://youtube.com',
                    description='Video sharing platform'
                )
            ]
            db.session.add_all(links)
            db.session.commit()
    
    def test_smart_link_categorization_model(self):
        """Test the SmartLinkCategorization model"""
        # Get test user and link
        user = User.query.filter_by(username='testuser').first()
        link = Link.query.filter_by(user_id=user.id).first()
        
        # Create a test categorization
        categorization = SmartLinkCategorization(
            user_id=user.id,
            link_id=link.id,
            suggested_category='Technology',
            confidence_score=0.95
        )
        db.session.add(categorization)
        db.session.commit()
        
        # Verify the categorization was created
        saved_categorization = SmartLinkCategorization.query.filter_by(
            user_id=user.id,
            link_id=link.id
        ).first()
        
        self.assertIsNotNone(saved_categorization)
        self.assertEqual(saved_categorization.suggested_category, 'Technology')
        self.assertEqual(saved_categorization.confidence_score, 0.95)
        self.assertFalse(saved_categorization.is_applied)
    
    def test_link_health_monitor_model(self):
        """Test the LinkHealthMonitor model"""
        # Get test user and link
        user = User.query.filter_by(username='testuser').first()
        link = Link.query.filter_by(user_id=user.id).first()
        
        # Create a test health monitor
        health_monitor = LinkHealthMonitor(
            user_id=user.id,
            link_id=link.id,
            status='healthy',
            response_time=0.5,
            status_code=200
        )
        issues = [
            {
                'type': 'warning',
                'description': 'Test warning',
                'severity': 'low'
            }
        ]
        health_monitor.set_issues(issues)
        db.session.add(health_monitor)
        db.session.commit()
        
        # Verify the health monitor was created
        saved_monitor = LinkHealthMonitor.query.filter_by(
            user_id=user.id,
            link_id=link.id
        ).first()
        
        self.assertIsNotNone(saved_monitor)
        self.assertEqual(saved_monitor.status, 'healthy')
        self.assertEqual(saved_monitor.response_time, 0.5)
        self.assertEqual(saved_monitor.status_code, 200)
        self.assertEqual(len(saved_monitor.get_issues()), 1)
        self.assertEqual(saved_monitor.get_issues()[0]['type'], 'warning')
    
    def test_security_scan_model(self):
        """Test the SecurityScan model"""
        # Get test user and link
        user = User.query.filter_by(username='testuser').first()
        link = Link.query.filter_by(user_id=user.id).first()
        
        # Create a test security scan
        security_scan = SecurityScan(
            user_id=user.id,
            link_id=link.id,
            security_score=0.85,
            risk_level='low_risk'
        )
        threats = [
            {
                'type': 'suspicious_redirect',
                'description': 'Test threat',
                'confidence': 0.7
            }
        ]
        security_scan.set_threats(threats)
        db.session.add(security_scan)
        db.session.commit()
        
        # Verify the security scan was created
        saved_scan = SecurityScan.query.filter_by(
            user_id=user.id,
            link_id=link.id
        ).first()
        
        self.assertIsNotNone(saved_scan)
        self.assertEqual(saved_scan.security_score, 0.85)
        self.assertEqual(saved_scan.risk_level, 'low_risk')
        self.assertEqual(len(saved_scan.get_threats()), 1)
        self.assertEqual(saved_scan.get_threats()[0]['type'], 'suspicious_redirect')
    
    def test_content_insight_model(self):
        """Test the ContentInsight model"""
        # Get test user and link
        user = User.query.filter_by(username='testuser').first()
        link = Link.query.filter_by(user_id=user.id).first()
        
        # Create a test content insight
        content_insight = ContentInsight(
            user_id=user.id,
            link_id=link.id,
            title='Test Title',
            description='Test Description',
            content_type='article'
        )
        keywords = ['test', 'ai', 'features']
        content_insight.set_keywords(keywords)
        content_insight.summary = 'Test summary'
        content_insight.sentiment_score = 0.7
        content_insight.reading_time = 300
        db.session.add(content_insight)
        db.session.commit()
        
        # Verify the content insight was created
        saved_insight = ContentInsight.query.filter_by(
            user_id=user.id,
            link_id=link.id
        ).first()
        
        self.assertIsNotNone(saved_insight)
        self.assertEqual(saved_insight.title, 'Test Title')
        self.assertEqual(saved_insight.content_type, 'article')
        self.assertEqual(saved_insight.get_keywords(), ['test', 'ai', 'features'])
        self.assertEqual(saved_insight.sentiment_score, 0.7)
        self.assertEqual(saved_insight.reading_time, 300)
    
    def test_audience_match_model(self):
        """Test the AudienceMatch model"""
        # Get test user and link
        user = User.query.filter_by(username='testuser').first()
        link = Link.query.filter_by(user_id=user.id).first()
        
        # Create a test audience match
        audience_match = AudienceMatch(
            user_id=user.id,
            link_id=link.id
        )
        audience_segments = {
            'age_groups': {
                '18-24': 0.3,
                '25-34': 0.4
            }
        }
        best_platforms = [
            {'name': 'LinkedIn', 'score': 0.9},
            {'name': 'Twitter', 'score': 0.8}
        ]
        optimal_times = {
            'Monday': ['09:00', '15:00'],
            'Wednesday': ['10:00']
        }
        audience_match.set_audience_segments(audience_segments)
        audience_match.set_best_platforms(best_platforms)
        audience_match.set_optimal_times(optimal_times)
        db.session.add(audience_match)
        db.session.commit()
        
        # Verify the audience match was created
        saved_match = AudienceMatch.query.filter_by(
            user_id=user.id,
            link_id=link.id
        ).first()
        
        self.assertIsNotNone(saved_match)
        self.assertEqual(saved_match.get_audience_segments()['age_groups']['18-24'], 0.3)
        self.assertEqual(len(saved_match.get_best_platforms()), 2)
        self.assertEqual(saved_match.get_best_platforms()[0]['name'], 'LinkedIn')
        self.assertEqual(len(saved_match.get_optimal_times()['Monday']), 2)
    
    def test_smart_link_preview_model(self):
        """Test the SmartLinkPreview model"""
        # Get test user and link
        user = User.query.filter_by(username='testuser').first()
        link = Link.query.filter_by(user_id=user.id).first()
        
        # Create a test smart preview
        smart_preview = SmartLinkPreview(
            user_id=user.id,
            link_id=link.id,
            title='Test Preview',
            description='Test Description',
            image_url='https://example.com/image.jpg',
            preview_type='enhanced'
        )
        custom_data = {
            'author': 'Test Author',
            'published_date': '2025-06-12T12:00:00',
            'read_time': '5 min read'
        }
        smart_preview.set_custom_data(custom_data)
        db.session.add(smart_preview)
        db.session.commit()
        
        # Verify the smart preview was created
        saved_preview = SmartLinkPreview.query.filter_by(
            user_id=user.id,
            link_id=link.id
        ).first()
        
        self.assertIsNotNone(saved_preview)
        self.assertEqual(saved_preview.title, 'Test Preview')
        self.assertEqual(saved_preview.preview_type, 'enhanced')
        self.assertEqual(saved_preview.get_custom_data()['author'], 'Test Author')
        self.assertEqual(saved_preview.get_custom_data()['read_time'], '5 min read')

if __name__ == '__main__':
    unittest.main()
