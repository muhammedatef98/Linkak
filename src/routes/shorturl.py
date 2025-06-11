from flask import Blueprint, request, redirect, render_template, jsonify, abort, url_for, current_app
from src.models.shorturl import ShortURL, URLAnalytics, db
from src.models.user import User
from datetime import datetime, timedelta
import validators
from flask_login import login_required, current_user
import json

shorturl_bp = Blueprint('shorturl', __name__)

@shorturl_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to create a shortened URL"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    original_url = data.get('url')
    custom_alias = data.get('custom_alias')
    domain = data.get('domain')
    expires_days = data.get('expires_days')
    
    # Validate URL
    if not validators.url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Set expiration date if provided
    expires_at = None
    if expires_days and isinstance(expires_days, int):
        expires_at = datetime.utcnow() + timedelta(days=expires_days)
    
    # Check if user is logged in
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
    
    # Check if custom alias is already taken
    if custom_alias:
        existing_alias = ShortURL.query.filter_by(custom_alias=custom_alias).first()
        if existing_alias:
            return jsonify({'error': 'Custom alias already in use'}), 409
    
    # Create new short URL
    try:
        short_url = ShortURL(
            original_url=original_url,
            user_id=user_id,
            custom_alias=custom_alias,
            domain=domain,
            expires_at=expires_at
        )
        db.session.add(short_url)
        db.session.commit()
        
        # Generate QR code
        qr_code_path = short_url.save_qr_code()
        
        return jsonify({
            'success': True,
            'data': {
                'original_url': short_url.original_url,
                'short_url': short_url.get_full_shortened_url(),
                'short_code': short_url.short_code,
                'qr_code': url_for('static', filename=f'qrcodes/{short_url.short_code}.png', _external=True),
                'expires_at': short_url.expires_at.isoformat() if short_url.expires_at else None,
                'created_at': short_url.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@shorturl_bp.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to the original URL from a short code"""
    # Find the short URL
    short_url = ShortURL.query.filter_by(short_code=short_code).first_or_404()
    
    # Check if URL is active and not expired
    if not short_url.is_active:
        abort(410)  # Gone
    
    if short_url.expires_at and short_url.expires_at < datetime.utcnow():
        abort(410)  # Gone
    
    # Record analytics
    analytics = URLAnalytics(
        short_url_id=short_url.id,
        referrer=request.referrer,
        user_agent=request.user_agent.string,
        ip_address=request.remote_addr
    )
    db.session.add(analytics)
    
    # Increment click count
    short_url.increment_click()
    
    # Redirect to the original URL
    return redirect(short_url.original_url)

@shorturl_bp.route('/dashboard/urls', methods=['GET'])
@login_required
def user_urls():
    """Display user's shortened URLs"""
    user_urls = ShortURL.query.filter_by(user_id=current_user.id).order_by(ShortURL.created_at.desc()).all()
    return render_template('dashboard/urls.html', urls=user_urls)

@shorturl_bp.route('/api/urls', methods=['GET'])
@login_required
def get_user_urls():
    """API endpoint to get user's shortened URLs"""
    user_urls = ShortURL.query.filter_by(user_id=current_user.id).order_by(ShortURL.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [url.to_dict() for url in user_urls]
    })

@shorturl_bp.route('/api/urls/<int:url_id>', methods=['GET'])
@login_required
def get_url_details(url_id):
    """API endpoint to get details of a specific shortened URL"""
    url = ShortURL.query.filter_by(id=url_id, user_id=current_user.id).first_or_404()
    
    # Get analytics data
    analytics = URLAnalytics.query.filter_by(short_url_id=url.id).order_by(URLAnalytics.click_time.desc()).all()
    
    # Prepare analytics summary
    summary = {
        'total_clicks': url.click_count,
        'devices': {},
        'browsers': {},
        'countries': {},
        'referrers': {},
        'clicks_over_time': {}
    }
    
    for entry in analytics:
        # Count by device type
        device = entry.device_type or 'unknown'
        summary['devices'][device] = summary['devices'].get(device, 0) + 1
        
        # Count by browser
        browser = entry.browser or 'unknown'
        summary['browsers'][browser] = summary['browsers'].get(browser, 0) + 1
        
        # Count by country
        country = entry.country or 'unknown'
        summary['countries'][country] = summary['countries'].get(country, 0) + 1
        
        # Count by referrer
        referrer = entry.referrer or 'direct'
        summary['referrers'][referrer] = summary['referrers'].get(referrer, 0) + 1
        
        # Count by date
        date_str = entry.click_time.strftime('%Y-%m-%d')
        summary['clicks_over_time'][date_str] = summary['clicks_over_time'].get(date_str, 0) + 1
    
    return jsonify({
        'success': True,
        'data': {
            'url': url.to_dict(),
            'analytics': {
                'summary': summary,
                'recent_clicks': [a.to_dict() for a in analytics[:10]]  # Last 10 clicks
            }
        }
    })

@shorturl_bp.route('/api/urls/<int:url_id>', methods=['PUT'])
@login_required
def update_url(url_id):
    """API endpoint to update a shortened URL"""
    url = ShortURL.query.filter_by(id=url_id, user_id=current_user.id).first_or_404()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'custom_alias' in data and data['custom_alias'] != url.custom_alias:
        # Check if new alias is available
        existing = ShortURL.query.filter_by(custom_alias=data['custom_alias']).first()
        if existing and existing.id != url.id:
            return jsonify({'error': 'Custom alias already in use'}), 409
        url.custom_alias = data['custom_alias']
        url.short_code = data['custom_alias']
    
    if 'domain' in data:
        url.domain = data['domain']
    
    if 'is_active' in data:
        url.is_active = bool(data['is_active'])
    
    if 'expires_days' in data:
        if data['expires_days']:
            url.expires_at = datetime.utcnow() + timedelta(days=int(data['expires_days']))
        else:
            url.expires_at = None
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': url.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@shorturl_bp.route('/api/urls/<int:url_id>', methods=['DELETE'])
@login_required
def delete_url(url_id):
    """API endpoint to delete a shortened URL"""
    url = ShortURL.query.filter_by(id=url_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(url)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@shorturl_bp.route('/api/domains', methods=['GET'])
@login_required
def get_user_domains():
    """API endpoint to get user's custom domains"""
    # In a real implementation, this would fetch from a domains table
    # For now, we'll return a placeholder
    return jsonify({
        'success': True,
        'data': [
            {'id': 1, 'domain': 'example.com', 'is_verified': True},
            {'id': 2, 'domain': 'mysite.org', 'is_verified': False}
        ]
    })

@shorturl_bp.route('/api/qrcode/<short_code>', methods=['GET'])
def get_qr_code(short_code):
    """API endpoint to get QR code for a shortened URL"""
    url = ShortURL.query.filter_by(short_code=short_code).first_or_404()
    
    # Generate QR code as base64 string
    qr_code_data = url.generate_qr_code()
    
    return jsonify({
        'success': True,
        'data': {
            'qr_code': qr_code_data
        }
    })
