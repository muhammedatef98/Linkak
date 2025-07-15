#!/usr/bin/env python3
"""
Linkak Database Manager
Handles database migrations, seeding, and maintenance tasks
"""

import os
import sys
import logging
import argparse
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main_production import create_app
from models.user import User, Link, db
from models.shorturl import ShortURL, URLAnalytics
from models.menu import Menu, MenuCategory, MenuItem
from models.advanced_features import AIRecommendation, AdvancedAnalytics, ScheduledContent, Collaboration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database management utility for Linkak"""
    
    def __init__(self):
        self.app = create_app()
        self.app_context = None
    
    def __enter__(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.app_context:
            self.app_context.pop()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully!")
            return True
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return False
    
    def drop_tables(self):
        """Drop all database tables (DANGEROUS!)"""
        try:
            logger.warning("Dropping all database tables...")
            db.drop_all()
            logger.info("All tables dropped successfully!")
            return True
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            return False
    
    def seed_demo_data(self):
        """Seed database with demo data"""
        try:
            logger.info("Seeding demo data...")
            
            # Check if demo user already exists
            demo_user = User.query.filter_by(username='demo').first()
            if demo_user:
                logger.info("Demo data already exists, skipping...")
                return True
            
            # Create demo user
            demo_user = User(
                username='demo',
                email='demo@linkak.com',
                password='password',  # Will be hashed automatically
                full_name='Demo User',
                bio='This is a demo account showcasing Linkak features.',
                is_verified=True
            )
            db.session.add(demo_user)
            db.session.flush()  # Get the user ID
            
            # Create demo links
            demo_links = [
                {
                    'title': 'My Portfolio Website',
                    'url': 'https://portfolio.example.com',
                    'icon': 'globe',
                    'category': 'Professional',
                    'is_featured': True,
                    'display_order': 1,
                    'description': 'Check out my latest work and projects'
                },
                {
                    'title': 'GitHub Profile',
                    'url': 'https://github.com/demo',
                    'icon': 'github',
                    'category': 'Professional',
                    'display_order': 2,
                    'description': 'My open source contributions'
                },
                {
                    'title': 'LinkedIn',
                    'url': 'https://linkedin.com/in/demo',
                    'icon': 'linkedin',
                    'category': 'Professional',
                    'is_featured': True,
                    'display_order': 3,
                    'description': 'Professional networking profile'
                },
                {
                    'title': 'Twitter',
                    'url': 'https://twitter.com/demo',
                    'icon': 'twitter',
                    'category': 'Social',
                    'display_order': 4,
                    'description': 'Follow me for tech updates'
                },
                {
                    'title': 'Blog',
                    'url': 'https://blog.example.com',
                    'icon': 'edit',
                    'category': 'Content',
                    'display_order': 5,
                    'description': 'My thoughts on technology and development'
                },
                {
                    'title': 'YouTube Channel',
                    'url': 'https://youtube.com/demo',
                    'icon': 'video',
                    'category': 'Content',
                    'display_order': 6,
                    'description': 'Tech tutorials and reviews'
                }
            ]
            
            for link_data in demo_links:
                link = Link(
                    user_id=demo_user.id,
                    **link_data
                )
                db.session.add(link)
            
            # Create demo short URL
            short_url = ShortURL(
                original_url='https://example.com/very/long/url/that/needs/shortening',
                user_id=demo_user.id,
                custom_alias='demo-url',
                description='Demo shortened URL'
            )
            db.session.add(short_url)
            db.session.flush()
            
            # Create demo menu
            menu = Menu(
                name='Demo Restaurant Menu',
                user_id=demo_user.id,
                business_name='Demo Café',
                description='Delicious food and beverages',
                theme='restaurant',
                contact_info='📞 (555) 123-4567\n📧 info@democafe.com',
                opening_hours='Mon-Fri: 8am-10pm\nSat-Sun: 9am-11pm'
            )
            db.session.add(menu)
            db.session.flush()
            
            # Create menu categories
            categories = [
                {
                    'name': 'Beverages',
                    'description': 'Hot and cold drinks',
                    'display_order': 1
                },
                {
                    'name': 'Appetizers',
                    'description': 'Light bites to start your meal',
                    'display_order': 2
                },
                {
                    'name': 'Main Courses',
                    'description': 'Hearty and satisfying meals',
                    'display_order': 3
                },
                {
                    'name': 'Desserts',
                    'description': 'Sweet treats to end your meal',
                    'display_order': 4
                }
            ]
            
            category_objects = []
            for cat_data in categories:
                category = MenuCategory(
                    menu_id=menu.id,
                    **cat_data
                )
                db.session.add(category)
                category_objects.append(category)
            
            db.session.flush()
            
            # Create menu items
            menu_items = [
                # Beverages
                {
                    'category_id': category_objects[0].id,
                    'name': 'Espresso',
                    'description': 'Rich and bold Italian espresso',
                    'price': 2.50,
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'category_id': category_objects[0].id,
                    'name': 'Cappuccino',
                    'description': 'Creamy espresso with steamed milk foam',
                    'price': 3.75,
                    'display_order': 2
                },
                {
                    'category_id': category_objects[0].id,
                    'name': 'Fresh Orange Juice',
                    'description': 'Freshly squeezed orange juice',
                    'price': 4.25,
                    'display_order': 3
                },
                # Appetizers
                {
                    'category_id': category_objects[1].id,
                    'name': 'Bruschetta',
                    'description': 'Toasted bread with tomatoes, basil, and garlic',
                    'price': 6.99,
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'category_id': category_objects[1].id,
                    'name': 'Hummus Plate',
                    'description': 'Homemade hummus with pita bread and vegetables',
                    'price': 7.50,
                    'display_order': 2
                },
                # Main Courses
                {
                    'category_id': category_objects[2].id,
                    'name': 'Grilled Salmon',
                    'description': 'Fresh Atlantic salmon with lemon herbs',
                    'price': 18.99,
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'category_id': category_objects[2].id,
                    'name': 'Chicken Caesar Salad',
                    'description': 'Crisp romaine lettuce with grilled chicken',
                    'price': 12.99,
                    'display_order': 2
                },
                {
                    'category_id': category_objects[2].id,
                    'name': 'Vegetable Pasta',
                    'description': 'Fresh pasta with seasonal vegetables',
                    'price': 14.50,
                    'display_order': 3
                },
                # Desserts
                {
                    'category_id': category_objects[3].id,
                    'name': 'Chocolate Cake',
                    'description': 'Rich chocolate cake with vanilla ice cream',
                    'price': 6.99,
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'category_id': category_objects[3].id,
                    'name': 'Tiramisu',
                    'description': 'Classic Italian dessert with coffee and mascarpone',
                    'price': 7.50,
                    'display_order': 2
                }
            ]
            
            for item_data in menu_items:
                item = MenuItem(**item_data)
                db.session.add(item)
            
            # Create demo analytics data
            analytics = AdvancedAnalytics(
                user_id=demo_user.id,
                metric_type='page_views',
                metric_value=150,
                date_recorded=datetime.utcnow().date()
            )
            db.session.add(analytics)
            
            # Create demo AI recommendation
            recommendation = AIRecommendation(
                user_id=demo_user.id,
                recommendation_type='layout',
                recommendation_data={
                    'suggestion': 'Consider reordering your links for better engagement',
                    'changes': [
                        {'type': 'move', 'item': 'featured_links', 'position': 'top'},
                        {'type': 'group', 'items': ['social_links'], 'label': 'Connect With Me'}
                    ],
                    'reasoning': 'Featured links at the top can increase click-through rates by 25%'
                },
                confidence_score=0.85
            )
            db.session.add(recommendation)
            
            # Commit all changes
            db.session.commit()
            logger.info("Demo data seeded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error seeding demo data: {e}")
            db.session.rollback()
            return False
    
    def create_admin_user(self, username, email, password):
        """Create an admin user"""
        try:
            # Check if user already exists
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                logger.error(f"User with username '{username}' or email '{email}' already exists!")
                return False
            
            # Create admin user
            admin_user = User(
                username=username,
                email=email,
                password=password,
                is_admin=True,
                is_verified=True,
                full_name='Administrator'
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            logger.info(f"Admin user '{username}' created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error creating admin user: {e}")
            db.session.rollback()
            return False
    
    def cleanup_old_data(self, days=30):
        """Clean up old data (analytics, logs, etc.)"""
        try:
            cutoff_date = datetime.utcnow().date() - timedelta(days=days)
            
            # Clean up old analytics data
            old_analytics = AdvancedAnalytics.query.filter(
                AdvancedAnalytics.date_recorded < cutoff_date
            ).all()
            
            for analytics in old_analytics:
                db.session.delete(analytics)
            
            # Clean up old URL analytics
            old_url_analytics = URLAnalytics.query.filter(
                URLAnalytics.accessed_at < cutoff_date
            ).all()
            
            for analytics in old_url_analytics:
                db.session.delete(analytics)
            
            db.session.commit()
            
            logger.info(f"Cleaned up {len(old_analytics)} analytics records and {len(old_url_analytics)} URL analytics records older than {days} days")
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            db.session.rollback()
            return False
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            stats = {
                'users': User.query.count(),
                'links': Link.query.count(),
                'short_urls': ShortURL.query.count(),
                'menus': Menu.query.count(),
                'menu_items': MenuItem.query.count(),
                'analytics_records': AdvancedAnalytics.query.count(),
                'url_analytics': URLAnalytics.query.count(),
                'ai_recommendations': AIRecommendation.query.count()
            }
            
            logger.info("Database Statistics:")
            for key, value in stats.items():
                logger.info(f"  {key.replace('_', ' ').title()}: {value}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def verify_database_integrity(self):
        """Verify database integrity"""
        try:
            logger.info("Verifying database integrity...")
            
            issues = []
            
            # Check for orphaned links
            orphaned_links = Link.query.filter(~Link.user_id.in_(
                db.session.query(User.id)
            )).count()
            
            if orphaned_links > 0:
                issues.append(f"Found {orphaned_links} orphaned links")
            
            # Check for orphaned short URLs
            orphaned_urls = ShortURL.query.filter(~ShortURL.user_id.in_(
                db.session.query(User.id)
            )).count()
            
            if orphaned_urls > 0:
                issues.append(f"Found {orphaned_urls} orphaned short URLs")
            
            # Check for orphaned menus
            orphaned_menus = Menu.query.filter(~Menu.user_id.in_(
                db.session.query(User.id)
            )).count()
            
            if orphaned_menus > 0:
                issues.append(f"Found {orphaned_menus} orphaned menus")
            
            if issues:
                logger.warning("Database integrity issues found:")
                for issue in issues:
                    logger.warning(f"  - {issue}")
                return False
            else:
                logger.info("Database integrity check passed!")
                return True
                
        except Exception as e:
            logger.error(f"Error verifying database integrity: {e}")
            return False


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Linkak Database Manager')
    parser.add_argument('action', choices=[
        'create', 'drop', 'seed', 'admin', 'cleanup', 'stats', 'verify'
    ], help='Action to perform')
    
    # Optional arguments for specific actions
    parser.add_argument('--username', help='Username for admin creation')
    parser.add_argument('--email', help='Email for admin creation')
    parser.add_argument('--password', help='Password for admin creation')
    parser.add_argument('--days', type=int, default=30, help='Days for cleanup (default: 30)')
    parser.add_argument('--force', action='store_true', help='Force dangerous operations')
    
    args = parser.parse_args()
    
    with DatabaseManager() as db_manager:
        if args.action == 'create':
            db_manager.create_tables()
            
        elif args.action == 'drop':
            if not args.force:
                confirm = input("This will delete ALL data! Type 'YES' to confirm: ")
                if confirm != 'YES':
                    logger.info("Operation cancelled")
                    return
            db_manager.drop_tables()
            
        elif args.action == 'seed':
            db_manager.seed_demo_data()
            
        elif args.action == 'admin':
            if not all([args.username, args.email, args.password]):
                logger.error("Username, email, and password are required for admin creation")
                return
            db_manager.create_admin_user(args.username, args.email, args.password)
            
        elif args.action == 'cleanup':
            db_manager.cleanup_old_data(args.days)
            
        elif args.action == 'stats':
            db_manager.get_database_stats()
            
        elif args.action == 'verify':
            db_manager.verify_database_integrity()


if __name__ == '__main__':
    main()