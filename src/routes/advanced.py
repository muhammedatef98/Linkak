from flask import Blueprint, request, jsonify
from src.models.advanced_features import AIRecommendation, AdvancedAnalytics, ScheduledContent, Collaboration, db
from src.models.user import User, Link
from flask_login import login_required, current_user
import json
from datetime import datetime, date, timedelta
import random

advanced_bp = Blueprint('advanced', __name__)

# AI Recommendations
@advanced_bp.route('/api/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """API endpoint to get AI recommendations for the user"""
    recommendations = AIRecommendation.query.filter_by(
        user_id=current_user.id, 
        is_applied=False
    ).order_by(AIRecommendation.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [rec.to_dict() for rec in recommendations]
    })

@advanced_bp.route('/api/recommendations/generate', methods=['POST'])
@login_required
def generate_recommendations():
    """API endpoint to generate new AI recommendations"""
    data = request.get_json()
    recommendation_type = data.get('type', 'all')
    
    # In a real implementation, this would call an AI service
    # For demo purposes, we'll generate mock recommendations
    
    new_recommendations = []
    
    if recommendation_type in ['all', 'layout']:
        # Generate layout recommendation
        layout_rec = AIRecommendation(
            user_id=current_user.id,
            recommendation_type='layout',
            recommendation_data={
                'suggestion': 'Optimize your profile layout for better engagement',
                'changes': [
                    {'type': 'move', 'item': 'featured_links', 'position': 'top'},
                    {'type': 'group', 'items': ['social_media_links'], 'label': 'Connect With Me'}
                ],
                'reasoning': 'Based on visitor behavior, featuring your most important links at the top can increase click-through rates by 30%.'
            }
        )
        db.session.add(layout_rec)
        new_recommendations.append(layout_rec)
    
    if recommendation_type in ['all', 'content']:
        # Generate content recommendation
        content_rec = AIRecommendation(
            user_id=current_user.id,
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
        db.session.add(content_rec)
        new_recommendations.append(content_rec)
    
    if recommendation_type in ['all', 'theme']:
        # Generate theme recommendation
        theme_rec = AIRecommendation(
            user_id=current_user.id,
            recommendation_type='theme',
            recommendation_data={
                'suggestion': 'Update your color scheme for better brand consistency',
                'changes': [
                    {'type': 'color', 'element': 'primary', 'value': '#3a86ff'},
                    {'type': 'color', 'element': 'secondary', 'value': '#8338ec'},
                    {'type': 'font', 'element': 'heading', 'value': 'Montserrat'}
                ],
                'reasoning': 'This color scheme aligns with your brand images and creates a more cohesive visual identity.'
            }
        )
        db.session.add(theme_rec)
        new_recommendations.append(theme_rec)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [rec.to_dict() for rec in new_recommendations]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/api/recommendations/<int:rec_id>/apply', methods=['POST'])
@login_required
def apply_recommendation(rec_id):
    """API endpoint to apply a recommendation"""
    recommendation = AIRecommendation.query.filter_by(
        id=rec_id, 
        user_id=current_user.id
    ).first_or_404()
    
    # In a real implementation, this would apply the changes to the user's profile
    # For demo purposes, we'll just mark it as applied
    
    recommendation.is_applied = True
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': recommendation.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Advanced Analytics
@advanced_bp.route('/api/analytics/summary', methods=['GET'])
@login_required
def get_analytics_summary():
    """API endpoint to get analytics summary"""
    # Get date range from query parameters
    days = int(request.args.get('days', 30))
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Get analytics for date range
    analytics = AdvancedAnalytics.query.filter(
        AdvancedAnalytics.user_id == current_user.id,
        AdvancedAnalytics.date >= start_date,
        AdvancedAnalytics.date <= end_date
    ).order_by(AdvancedAnalytics.date).all()
    
    # If no analytics exist, generate mock data
    if not analytics:
        analytics = generate_mock_analytics(current_user.id, start_date, end_date)
    
    # Calculate summary metrics
    total_views = sum(a.total_views for a in analytics)
    total_visitors = sum(a.unique_visitors for a in analytics)
    avg_bounce_rate = sum(a.bounce_rate or 0 for a in analytics) / len(analytics) if analytics else 0
    avg_time_on_page = sum(a.avg_time_on_page or 0 for a in analytics) / len(analytics) if analytics else 0
    
    # Aggregate device data
    device_data = {}
    for a in analytics:
        for device, count in a.get_device_data().items():
            device_data[device] = device_data.get(device, 0) + count
    
    # Aggregate location data
    location_data = {}
    for a in analytics:
        for location, count in a.get_location_data().items():
            location_data[location] = location_data.get(location, 0) + count
    
    # Aggregate referrer data
    referrer_data = {}
    for a in analytics:
        for referrer, count in a.get_referrer_data().items():
            referrer_data[referrer] = referrer_data.get(referrer, 0) + count
    
    # Prepare time series data
    time_series = [{
        'date': a.date.isoformat(),
        'views': a.total_views,
        'visitors': a.unique_visitors,
        'bounce_rate': a.bounce_rate
    } for a in analytics]
    
    return jsonify({
        'success': True,
        'data': {
            'summary': {
                'total_views': total_views,
                'total_visitors': total_visitors,
                'avg_bounce_rate': avg_bounce_rate,
                'avg_time_on_page': avg_time_on_page
            },
            'device_data': device_data,
            'location_data': location_data,
            'referrer_data': referrer_data,
            'time_series': time_series
        }
    })

def generate_mock_analytics(user_id, start_date, end_date):
    """Generate mock analytics data for demo purposes"""
    analytics = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate random but realistic data
        views = random.randint(50, 200)
        visitors = random.randint(30, views)
        bounce_rate = random.uniform(0.3, 0.7)
        avg_time = random.uniform(30, 180)
        
        # Create device breakdown
        device_data = {
            'desktop': int(views * random.uniform(0.4, 0.6)),
            'mobile': int(views * random.uniform(0.3, 0.5)),
            'tablet': int(views * random.uniform(0.05, 0.15))
        }
        
        # Create location breakdown
        location_data = {
            'United States': int(views * random.uniform(0.3, 0.5)),
            'United Kingdom': int(views * random.uniform(0.1, 0.2)),
            'Canada': int(views * random.uniform(0.05, 0.15)),
            'Germany': int(views * random.uniform(0.05, 0.1)),
            'Other': int(views * random.uniform(0.1, 0.2))
        }
        
        # Create referrer breakdown
        referrer_data = {
            'Direct': int(views * random.uniform(0.3, 0.5)),
            'Google': int(views * random.uniform(0.2, 0.4)),
            'Twitter': int(views * random.uniform(0.05, 0.15)),
            'Instagram': int(views * random.uniform(0.05, 0.15)),
            'Other': int(views * random.uniform(0.05, 0.1))
        }
        
        # Create analytics record
        analytics_record = AdvancedAnalytics(
            user_id=user_id,
            date=current_date,
            total_views=views,
            unique_visitors=visitors,
            bounce_rate=bounce_rate,
            avg_time_on_page=avg_time
        )
        
        analytics_record.set_device_data(device_data)
        analytics_record.set_location_data(location_data)
        analytics_record.set_referrer_data(referrer_data)
        
        db.session.add(analytics_record)
        analytics.append(analytics_record)
        
        current_date += timedelta(days=1)
    
    try:
        db.session.commit()
        return analytics
    except Exception:
        db.session.rollback()
        return []

# Scheduled Content
@advanced_bp.route('/api/scheduled', methods=['GET'])
@login_required
def get_scheduled_content():
    """API endpoint to get scheduled content"""
    scheduled = ScheduledContent.query.filter_by(
        user_id=current_user.id,
        is_executed=False
    ).order_by(ScheduledContent.scheduled_time).all()
    
    return jsonify({
        'success': True,
        'data': [s.to_dict() for s in scheduled]
    })

@advanced_bp.route('/api/scheduled', methods=['POST'])
@login_required
def create_scheduled_content():
    """API endpoint to create scheduled content"""
    data = request.get_json()
    
    if not data or 'content_type' not in data or 'action' not in data or 'scheduled_time' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        scheduled_time = datetime.fromisoformat(data['scheduled_time'])
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400
    
    # Create scheduled content
    try:
        scheduled = ScheduledContent(
            user_id=current_user.id,
            content_type=data['content_type'],
            action=data['action'],
            scheduled_time=scheduled_time,
            content_id=data.get('content_id'),
            content_data=data.get('content_data')
        )
        
        db.session.add(scheduled)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': scheduled.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/api/scheduled/<int:scheduled_id>', methods=['DELETE'])
@login_required
def delete_scheduled_content(scheduled_id):
    """API endpoint to delete scheduled content"""
    scheduled = ScheduledContent.query.filter_by(
        id=scheduled_id,
        user_id=current_user.id
    ).first_or_404()
    
    try:
        db.session.delete(scheduled)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Collaboration
@advanced_bp.route('/api/collaborations', methods=['GET'])
@login_required
def get_collaborations():
    """API endpoint to get collaborations"""
    # Get collaborations where user is the owner
    owned = Collaboration.query.filter_by(owner_id=current_user.id).all()
    
    # Get collaborations where user is a collaborator
    invited = Collaboration.query.filter_by(collaborator_id=current_user.id).all()
    
    return jsonify({
        'success': True,
        'data': {
            'owned': [c.to_dict() for c in owned],
            'invited': [c.to_dict() for c in invited]
        }
    })

@advanced_bp.route('/api/collaborations', methods=['POST'])
@login_required
def create_collaboration():
    """API endpoint to create a collaboration"""
    data = request.get_json()
    
    if not data or 'collaborator_email' not in data or 'resource_type' not in data or 'resource_id' not in data or 'permission_level' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Find collaborator by email
    collaborator = User.query.filter_by(email=data['collaborator_email']).first()
    if not collaborator:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if collaboration already exists
    existing = Collaboration.query.filter_by(
        owner_id=current_user.id,
        collaborator_id=collaborator.id,
        resource_type=data['resource_type'],
        resource_id=data['resource_id']
    ).first()
    
    if existing:
        return jsonify({'error': 'Collaboration already exists'}), 409
    
    # Create collaboration
    try:
        collaboration = Collaboration(
            owner_id=current_user.id,
            collaborator_id=collaborator.id,
            resource_type=data['resource_type'],
            resource_id=data['resource_id'],
            permission_level=data['permission_level']
        )
        
        db.session.add(collaboration)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': collaboration.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/api/collaborations/<int:collab_id>', methods=['PUT'])
@login_required
def update_collaboration(collab_id):
    """API endpoint to update a collaboration"""
    collaboration = Collaboration.query.filter_by(
        id=collab_id,
        owner_id=current_user.id
    ).first_or_404()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update permission level
    if 'permission_level' in data:
        collaboration.permission_level = data['permission_level']
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': collaboration.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@advanced_bp.route('/api/collaborations/<int:collab_id>', methods=['DELETE'])
@login_required
def delete_collaboration(collab_id):
    """API endpoint to delete a collaboration"""
    collaboration = Collaboration.query.filter_by(
        id=collab_id,
        owner_id=current_user.id
    ).first_or_404()
    
    try:
        db.session.delete(collaboration)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
