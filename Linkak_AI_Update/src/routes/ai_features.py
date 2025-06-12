from flask import Blueprint, request, jsonify
from src.models.ai_features import (
    SmartLinkCategorization, LinkHealthMonitor, SecurityScan, 
    ContentInsight, AudienceMatch, SmartLinkPreview, db
)
from src.models.user import User, Link
from flask_login import login_required, current_user
import json
from datetime import datetime, timedelta
import random
import requests
from urllib.parse import urlparse
import time

ai_features_bp = Blueprint('ai_features', __name__)

# Smart Link Categorization
@ai_features_bp.route('/api/ai/categorize', methods=['POST'])
@login_required
def categorize_links():
    """API endpoint to categorize links using AI"""
    data = request.get_json()
    link_ids = data.get('link_ids', [])
    
    if not link_ids:
        # If no specific links provided, get all uncategorized links
        links = Link.query.filter_by(user_id=current_user.id).all()
        link_ids = [link.id for link in links]
    
    results = []
    for link_id in link_ids:
        link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
        if not link:
            continue
        
        # In a real implementation, this would call an AI service
        # For demo purposes, we'll generate mock categorizations
        categories = [
            'Professional', 'Social Media', 'Portfolio', 'Blog', 
            'E-commerce', 'Documentation', 'Video', 'Music',
            'Education', 'News', 'Technology', 'Health', 'Finance'
        ]
        
        # Generate a "smart" category based on the URL and title
        url_parts = urlparse(link.url)
        domain = url_parts.netloc.lower()
        
        # Simple rule-based categorization for demo
        suggested_category = 'Other'
        confidence = random.uniform(0.7, 0.95)
        
        if 'github' in domain or 'gitlab' in domain:
            suggested_category = 'Development'
            confidence = random.uniform(0.85, 0.98)
        elif 'linkedin' in domain:
            suggested_category = 'Professional'
            confidence = random.uniform(0.9, 0.99)
        elif 'youtube' in domain or 'vimeo' in domain:
            suggested_category = 'Video'
            confidence = random.uniform(0.9, 0.99)
        elif 'instagram' in domain or 'facebook' in domain or 'twitter' in domain:
            suggested_category = 'Social Media'
            confidence = random.uniform(0.9, 0.99)
        elif 'medium' in domain or 'blog' in domain or 'wordpress' in domain:
            suggested_category = 'Blog'
            confidence = random.uniform(0.85, 0.95)
        elif 'shop' in domain or 'store' in domain or 'amazon' in domain or 'etsy' in domain:
            suggested_category = 'E-commerce'
            confidence = random.uniform(0.85, 0.95)
        elif 'docs' in domain or 'documentation' in domain:
            suggested_category = 'Documentation'
            confidence = random.uniform(0.85, 0.95)
        elif 'edu' in domain or 'course' in domain or 'learn' in domain:
            suggested_category = 'Education'
            confidence = random.uniform(0.85, 0.95)
        elif 'news' in domain or 'article' in domain:
            suggested_category = 'News'
            confidence = random.uniform(0.8, 0.95)
        else:
            # Random category with lower confidence
            suggested_category = random.choice(categories)
            confidence = random.uniform(0.6, 0.8)
        
        # Create or update categorization
        categorization = SmartLinkCategorization.query.filter_by(
            user_id=current_user.id,
            link_id=link.id
        ).first()
        
        if categorization:
            categorization.suggested_category = suggested_category
            categorization.confidence_score = confidence
        else:
            categorization = SmartLinkCategorization(
                user_id=current_user.id,
                link_id=link.id,
                suggested_category=suggested_category,
                confidence_score=confidence
            )
            db.session.add(categorization)
        
        results.append(categorization)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_features_bp.route('/api/ai/categorize/<int:categorization_id>/apply', methods=['POST'])
@login_required
def apply_categorization(categorization_id):
    """API endpoint to apply a suggested categorization"""
    categorization = SmartLinkCategorization.query.filter_by(
        id=categorization_id,
        user_id=current_user.id
    ).first_or_404()
    
    link = Link.query.filter_by(id=categorization.link_id).first_or_404()
    link.category = categorization.suggested_category
    categorization.is_applied = True
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': categorization.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Link Health Monitoring
@ai_features_bp.route('/api/ai/health-check', methods=['POST'])
@login_required
def check_link_health():
    """API endpoint to check link health"""
    data = request.get_json()
    link_ids = data.get('link_ids', [])
    
    if not link_ids:
        # If no specific links provided, get all links
        links = Link.query.filter_by(user_id=current_user.id).all()
        link_ids = [link.id for link in links]
    
    results = []
    for link_id in link_ids:
        link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
        if not link:
            continue
        
        # In a real implementation, this would make actual HTTP requests
        # For demo purposes, we'll generate mock health data
        
        # Simulate different health statuses
        statuses = ['healthy', 'broken', 'redirected', 'slow', 'warning']
        weights = [0.7, 0.05, 0.1, 0.1, 0.05]  # Most links should be healthy
        status = random.choices(statuses, weights=weights, k=1)[0]
        
        response_time = None
        status_code = None
        redirect_url = None
        issues = []
        
        if status == 'healthy':
            response_time = random.uniform(0.1, 1.0)
            status_code = 200
        elif status == 'broken':
            response_time = random.uniform(0.1, 3.0)
            status_code = random.choice([404, 500, 503])
            issues.append({
                'type': 'broken_link',
                'description': f'Link returns {status_code} status code',
                'severity': 'high'
            })
        elif status == 'redirected':
            response_time = random.uniform(0.1, 2.0)
            status_code = random.choice([301, 302, 307])
            parsed_url = urlparse(link.url)
            redirect_url = f"{parsed_url.scheme}://new.{parsed_url.netloc}{parsed_url.path}"
            issues.append({
                'type': 'redirect',
                'description': f'Link redirects to {redirect_url}',
                'severity': 'medium'
            })
        elif status == 'slow':
            response_time = random.uniform(3.0, 8.0)
            status_code = 200
            issues.append({
                'type': 'slow_response',
                'description': f'Link response time is {response_time:.2f} seconds',
                'severity': 'medium'
            })
        elif status == 'warning':
            response_time = random.uniform(0.1, 2.0)
            status_code = 200
            issues.append({
                'type': 'content_warning',
                'description': 'Link content may have changed significantly',
                'severity': 'low'
            })
        
        # Create or update health monitor
        health_monitor = LinkHealthMonitor.query.filter_by(
            user_id=current_user.id,
            link_id=link.id
        ).first()
        
        if health_monitor:
            health_monitor.last_checked = datetime.utcnow()
            health_monitor.status = status
            health_monitor.response_time = response_time
            health_monitor.status_code = status_code
            health_monitor.redirect_url = redirect_url
            health_monitor.set_issues(issues)
        else:
            health_monitor = LinkHealthMonitor(
                user_id=current_user.id,
                link_id=link.id,
                status=status,
                response_time=response_time,
                status_code=status_code,
                redirect_url=redirect_url
            )
            health_monitor.set_issues(issues)
            db.session.add(health_monitor)
        
        results.append(health_monitor)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Security Scanning
@ai_features_bp.route('/api/ai/security-scan', methods=['POST'])
@login_required
def scan_link_security():
    """API endpoint to scan links for security issues"""
    data = request.get_json()
    link_ids = data.get('link_ids', [])
    
    if not link_ids:
        # If no specific links provided, get all links
        links = Link.query.filter_by(user_id=current_user.id).all()
        link_ids = [link.id for link in links]
    
    results = []
    for link_id in link_ids:
        link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
        if not link:
            continue
        
        # In a real implementation, this would call a security scanning service
        # For demo purposes, we'll generate mock security data
        
        # Most links should be safe
        risk_levels = ['safe', 'low_risk', 'medium_risk', 'high_risk', 'dangerous']
        weights = [0.8, 0.1, 0.05, 0.03, 0.02]
        risk_level = random.choices(risk_levels, weights=weights, k=1)[0]
        
        # Security score based on risk level
        security_scores = {
            'safe': random.uniform(0.9, 1.0),
            'low_risk': random.uniform(0.7, 0.89),
            'medium_risk': random.uniform(0.5, 0.69),
            'high_risk': random.uniform(0.3, 0.49),
            'dangerous': random.uniform(0.0, 0.29)
        }
        security_score = security_scores[risk_level]
        
        threats = []
        if risk_level != 'safe':
            possible_threats = [
                {
                    'type': 'phishing',
                    'description': 'This link may be attempting to steal personal information',
                    'confidence': random.uniform(0.7, 0.95)
                },
                {
                    'type': 'malware',
                    'description': 'This link may contain or distribute malicious software',
                    'confidence': random.uniform(0.7, 0.95)
                },
                {
                    'type': 'spam',
                    'description': 'This link may lead to unwanted or unsolicited content',
                    'confidence': random.uniform(0.7, 0.95)
                },
                {
                    'type': 'unsafe_content',
                    'description': 'This link may contain inappropriate or unsafe content',
                    'confidence': random.uniform(0.7, 0.95)
                },
                {
                    'type': 'suspicious_redirect',
                    'description': 'This link may redirect to an unsafe destination',
                    'confidence': random.uniform(0.7, 0.95)
                }
            ]
            
            # Add 1-3 threats based on risk level
            num_threats = {
                'low_risk': 1,
                'medium_risk': random.randint(1, 2),
                'high_risk': random.randint(2, 3),
                'dangerous': random.randint(2, 3)
            }
            
            threats = random.sample(possible_threats, num_threats.get(risk_level, 0))
        
        # Create or update security scan
        security_scan = SecurityScan.query.filter_by(
            user_id=current_user.id,
            link_id=link.id
        ).first()
        
        if security_scan:
            security_scan.scan_date = datetime.utcnow()
            security_scan.security_score = security_score
            security_scan.risk_level = risk_level
            security_scan.set_threats(threats)
        else:
            security_scan = SecurityScan(
                user_id=current_user.id,
                link_id=link.id,
                security_score=security_score,
                risk_level=risk_level
            )
            security_scan.set_threats(threats)
            db.session.add(security_scan)
        
        results.append(security_scan)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Content Insights
@ai_features_bp.route('/api/ai/content-insights', methods=['POST'])
@login_required
def analyze_content():
    """API endpoint to analyze link content and provide insights"""
    data = request.get_json()
    link_ids = data.get('link_ids', [])
    
    if not link_ids:
        # If no specific links provided, get all links
        links = Link.query.filter_by(user_id=current_user.id).all()
        link_ids = [link.id for link in links]
    
    results = []
    for link_id in link_ids:
        link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
        if not link:
            continue
        
        # In a real implementation, this would scrape and analyze the content
        # For demo purposes, we'll generate mock content insights
        
        # Generate title if not already set
        title = link.title or f"Content about {random.choice(['technology', 'business', 'education', 'entertainment', 'health'])}"
        
        # Generate description
        descriptions = [
            "An in-depth article exploring the latest trends and innovations.",
            "A comprehensive guide to understanding key concepts and strategies.",
            "A detailed analysis of important factors and considerations.",
            "A collection of best practices and expert recommendations.",
            "An overview of essential information and practical applications."
        ]
        description = random.choice(descriptions)
        
        # Generate content type
        content_types = ['article', 'product', 'video', 'service', 'tool', 'documentation', 'social']
        content_type = random.choice(content_types)
        
        # Generate keywords
        keyword_sets = [
            ['innovation', 'technology', 'digital', 'future', 'trends'],
            ['business', 'strategy', 'growth', 'marketing', 'success'],
            ['education', 'learning', 'skills', 'knowledge', 'development'],
            ['health', 'wellness', 'fitness', 'nutrition', 'lifestyle'],
            ['design', 'creativity', 'inspiration', 'art', 'visual']
        ]
        keywords = random.choice(keyword_sets)
        
        # Generate summary
        summaries = [
            "This content provides valuable insights into important topics, offering practical advice and actionable recommendations.",
            "The page presents a detailed exploration of key concepts, with evidence-based information and expert perspectives.",
            "This resource offers comprehensive coverage of essential information, with clear explanations and helpful examples.",
            "The content delivers a thorough analysis of relevant factors, highlighting important considerations and potential implications.",
            "This page features an accessible overview of complex topics, making difficult concepts easier to understand."
        ]
        summary = random.choice(summaries)
        
        # Generate sentiment score (-1.0 to 1.0)
        sentiment_score = random.uniform(-0.3, 0.8)  # Slightly biased toward positive
        
        # Generate reading time (in seconds)
        reading_time = random.randint(60, 900)  # 1-15 minutes
        
        # Create or update content insight
        content_insight = ContentInsight.query.filter_by(
            user_id=current_user.id,
            link_id=link.id
        ).first()
        
        if content_insight:
            content_insight.analysis_date = datetime.utcnow()
            content_insight.title = title
            content_insight.description = description
            content_insight.content_type = content_type
            content_insight.set_keywords(keywords)
            content_insight.summary = summary
            content_insight.sentiment_score = sentiment_score
            content_insight.reading_time = reading_time
        else:
            content_insight = ContentInsight(
                user_id=current_user.id,
                link_id=link.id,
                title=title,
                description=description,
                content_type=content_type
            )
            content_insight.set_keywords(keywords)
            content_insight.summary = summary
            content_insight.sentiment_score = sentiment_score
            content_insight.reading_time = reading_time
            db.session.add(content_insight)
        
        results.append(content_insight)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Audience Matching
@ai_features_bp.route('/api/ai/audience-match', methods=['POST'])
@login_required
def match_audience():
    """API endpoint to match content with optimal audience and platforms"""
    data = request.get_json()
    link_ids = data.get('link_ids', [])
    
    if not link_ids:
        # If no specific links provided, get all links
        links = Link.query.filter_by(user_id=current_user.id).all()
        link_ids = [link.id for link in links]
    
    results = []
    for link_id in link_ids:
        link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
        if not link:
            continue
        
        # In a real implementation, this would use AI to analyze content and match with audience
        # For demo purposes, we'll generate mock audience matching data
        
        # Generate audience segments
        audience_segments = {
            'age_groups': {
                '18-24': random.uniform(0.1, 0.3),
                '25-34': random.uniform(0.2, 0.4),
                '35-44': random.uniform(0.15, 0.3),
                '45-54': random.uniform(0.05, 0.2),
                '55+': random.uniform(0.05, 0.15)
            },
            'interests': [
                {'name': 'Technology', 'relevance': random.uniform(0.6, 1.0)},
                {'name': 'Business', 'relevance': random.uniform(0.5, 0.9)},
                {'name': 'Education', 'relevance': random.uniform(0.4, 0.8)},
                {'name': 'Entertainment', 'relevance': random.uniform(0.3, 0.7)}
            ],
            'education_level': {
                'high_school': random.uniform(0.1, 0.3),
                'bachelors': random.uniform(0.3, 0.5),
                'masters': random.uniform(0.2, 0.4),
                'doctorate': random.uniform(0.05, 0.2)
            },
            'industry': [
                {'name': 'Technology', 'relevance': random.uniform(0.6, 1.0)},
                {'name': 'Finance', 'relevance': random.uniform(0.4, 0.8)},
                {'name': 'Education', 'relevance': random.uniform(0.3, 0.7)},
                {'name': 'Healthcare', 'relevance': random.uniform(0.2, 0.6)}
            ]
        }
        
        # Generate best platforms
        platforms = [
            {'name': 'LinkedIn', 'score': random.uniform(0.5, 1.0), 'reason': 'Professional audience alignment'},
            {'name': 'Twitter', 'score': random.uniform(0.4, 0.9), 'reason': 'Good for short-form content sharing'},
            {'name': 'Facebook', 'score': random.uniform(0.3, 0.8), 'reason': 'Wide demographic reach'},
            {'name': 'Instagram', 'score': random.uniform(0.2, 0.7), 'reason': 'Visual content performs well'},
            {'name': 'Reddit', 'score': random.uniform(0.3, 0.8), 'reason': 'Topic-focused communities'},
            {'name': 'Email', 'score': random.uniform(0.5, 0.9), 'reason': 'Direct engagement with subscribers'}
        ]
        # Sort by score and take top 3-4
        platforms.sort(key=lambda x: x['score'], reverse=True)
        best_platforms = platforms[:random.randint(3, 4)]
        
        # Generate optimal posting times
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        optimal_times = {}
        
        for day in days:
            # Generate 1-3 optimal time slots per day
            time_slots = []
            for _ in range(random.randint(1, 3)):
                hour = random.randint(8, 20)
                minute = random.choice([0, 15, 30, 45])
                time_slots.append(f"{hour:02d}:{minute:02d}")
            
            optimal_times[day] = time_slots
        
        # Create or update audience match
        audience_match = AudienceMatch.query.filter_by(
            user_id=current_user.id,
            link_id=link.id
        ).first()
        
        if audience_match:
            audience_match.analysis_date = datetime.utcnow()
            audience_match.set_audience_segments(audience_segments)
            audience_match.set_best_platforms(best_platforms)
            audience_match.set_optimal_times(optimal_times)
        else:
            audience_match = AudienceMatch(
                user_id=current_user.id,
                link_id=link.id
            )
            audience_match.set_audience_segments(audience_segments)
            audience_match.set_best_platforms(best_platforms)
            audience_match.set_optimal_times(optimal_times)
            db.session.add(audience_match)
        
        results.append(audience_match)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Smart Link Previews
@ai_features_bp.route('/api/ai/smart-preview', methods=['POST'])
@login_required
def generate_smart_preview():
    """API endpoint to generate enhanced link previews"""
    data = request.get_json()
    link_ids = data.get('link_ids', [])
    preview_type = data.get('preview_type', 'standard')
    
    if not link_ids:
        # If no specific links provided, get all links
        links = Link.query.filter_by(user_id=current_user.id).all()
        link_ids = [link.id for link in links]
    
    results = []
    for link_id in link_ids:
        link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
        if not link:
            continue
        
        # In a real implementation, this would scrape the page and generate a preview
        # For demo purposes, we'll generate mock preview data
        
        # Generate title if not already set
        title = link.title or f"Content about {random.choice(['technology', 'business', 'education', 'entertainment', 'health'])}"
        
        # Generate description
        descriptions = [
            "An in-depth article exploring the latest trends and innovations.",
            "A comprehensive guide to understanding key concepts and strategies.",
            "A detailed analysis of important factors and considerations.",
            "A collection of best practices and expert recommendations.",
            "An overview of essential information and practical applications."
        ]
        description = random.choice(descriptions)
        
        # Generate image URL
        image_url = f"https://picsum.photos/seed/{link.id}/800/400"
        
        # Generate favicon URL
        parsed_url = urlparse(link.url)
        favicon_url = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
        
        # Generate custom data based on preview type
        custom_data = {}
        if preview_type == 'enhanced':
            custom_data = {
                'author': f"Author {random.randint(1, 100)}",
                'published_date': (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
                'read_time': f"{random.randint(3, 15)} min read",
                'topic': random.choice(['Technology', 'Business', 'Education', 'Health', 'Entertainment']),
                'engagement': {
                    'likes': random.randint(10, 1000),
                    'shares': random.randint(5, 500),
                    'comments': random.randint(0, 100)
                }
            }
        elif preview_type == 'custom':
            # Custom preview for specific types of content
            content_types = ['product', 'article', 'video', 'event', 'job']
            content_type = random.choice(content_types)
            
            if content_type == 'product':
                custom_data = {
                    'price': f"${random.randint(10, 1000)}.{random.randint(0, 99):02d}",
                    'rating': round(random.uniform(3.0, 5.0), 1),
                    'reviews': random.randint(5, 500),
                    'availability': random.choice(['In Stock', 'Limited Stock', 'Pre-order']),
                    'shipping': random.choice(['Free Shipping', '2-Day Shipping', 'Standard Shipping'])
                }
            elif content_type == 'article':
                custom_data = {
                    'author': f"Author {random.randint(1, 100)}",
                    'published_date': (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
                    'read_time': f"{random.randint(3, 15)} min read",
                    'publication': random.choice(['Tech Today', 'Business Weekly', 'Education Times', 'Health Magazine']),
                    'topics': random.sample(['Technology', 'Business', 'Education', 'Health', 'Entertainment'], k=random.randint(1, 3))
                }
            elif content_type == 'video':
                custom_data = {
                    'duration': f"{random.randint(1, 120)}:{random.randint(0, 59):02d}",
                    'views': random.randint(100, 1000000),
                    'channel': f"Channel {random.randint(1, 100)}",
                    'published_date': (datetime.utcnow() - timedelta(days=random.randint(1, 365))).isoformat()
                }
            elif content_type == 'event':
                custom_data = {
                    'date': (datetime.utcnow() + timedelta(days=random.randint(1, 90))).isoformat(),
                    'location': random.choice(['New York', 'San Francisco', 'London', 'Tokyo', 'Berlin']),
                    'organizer': f"Organizer {random.randint(1, 100)}",
                    'attendees': random.randint(10, 1000),
                    'type': random.choice(['Conference', 'Workshop', 'Webinar', 'Meetup', 'Hackathon'])
                }
            elif content_type == 'job':
                custom_data = {
                    'company': f"Company {random.randint(1, 100)}",
                    'location': random.choice(['New York', 'San Francisco', 'London', 'Tokyo', 'Berlin', 'Remote']),
                    'salary': f"${random.randint(50, 200)}k - ${random.randint(201, 300)}k",
                    'posted_date': (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
                    'job_type': random.choice(['Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship'])
                }
            
            custom_data['content_type'] = content_type
        
        # Create or update smart preview
        smart_preview = SmartLinkPreview.query.filter_by(
            user_id=current_user.id,
            link_id=link.id
        ).first()
        
        if smart_preview:
            smart_preview.generated_at = datetime.utcnow()
            smart_preview.title = title
            smart_preview.description = description
            smart_preview.image_url = image_url
            smart_preview.favicon_url = favicon_url
            smart_preview.preview_type = preview_type
            smart_preview.set_custom_data(custom_data)
        else:
            smart_preview = SmartLinkPreview(
                user_id=current_user.id,
                link_id=link.id,
                title=title,
                description=description,
                image_url=image_url,
                preview_type=preview_type
            )
            smart_preview.favicon_url = favicon_url
            smart_preview.set_custom_data(custom_data)
            db.session.add(smart_preview)
        
        results.append(smart_preview)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
