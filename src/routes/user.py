from flask import Blueprint, request, render_template, jsonify, redirect, url_for, abort
from src.models.user import User, Link, db
from src.models.menu import Menu
from src.models.shorturl import ShortURL
from flask_login import login_required, current_user
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """API endpoint to get user profile"""
    return jsonify({
        'success': True,
        'data': current_user.to_dict(include_private=True)
    })

@user_bp.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    """API endpoint to update user profile"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    
    if 'bio' in data:
        current_user.bio = data['bio']
    
    if 'theme' in data:
        current_user.theme = data['theme']
    
    if 'social_links' in data:
        current_user.set_social_links(data['social_links'])
    
    if 'custom_domain' in data:
        current_user.custom_domain = data['custom_domain']
    
    if 'profile_settings' in data:
        current_user.set_profile_settings(data['profile_settings'])
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': current_user.to_dict(include_private=True)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/profile/image', methods=['POST'])
@login_required
def update_profile_image():
    """API endpoint to update profile image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400
    
    # Save image
    filename = secure_filename(image_file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{filename}"
    
    # Create directory if it doesn't exist
    upload_dir = os.path.join('src/static/uploads/profiles')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, filename)
    image_file.save(file_path)
    
    # Update user profile
    current_user.profile_image = f"/static/uploads/profiles/{filename}"
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': {
                'profile_image': current_user.profile_image
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/links', methods=['GET'])
@login_required
def get_user_links():
    """API endpoint to get user's links"""
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.display_order).all()
    return jsonify({
        'success': True,
        'data': [link.to_dict() for link in links]
    })

@user_bp.route('/api/links', methods=['POST'])
@login_required
def create_link():
    """API endpoint to create a new link"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'url' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create new link
    try:
        link = Link(
            title=data.get('title'),
            url=data.get('url'),
            user_id=current_user.id,
            description=data.get('description'),
            icon=data.get('icon'),
            custom_image=data.get('custom_image'),
            category=data.get('category'),
            is_featured=data.get('is_featured', False),
            display_order=data.get('display_order', 0),
            link_type=data.get('link_type', 'standard'),
            reference_id=data.get('reference_id')
        )
        
        # Set additional settings if provided
        if 'settings' in data:
            link.set_settings(data['settings'])
        
        db.session.add(link)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': link.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/links/<int:link_id>', methods=['PUT'])
@login_required
def update_link(link_id):
    """API endpoint to update a link"""
    link = Link.query.filter_by(id=link_id, user_id=current_user.id).first_or_404()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'title' in data:
        link.title = data['title']
    
    if 'url' in data:
        link.url = data['url']
    
    if 'description' in data:
        link.description = data['description']
    
    if 'icon' in data:
        link.icon = data['icon']
    
    if 'custom_image' in data:
        link.custom_image = data['custom_image']
    
    if 'category' in data:
        link.category = data['category']
    
    if 'is_active' in data:
        link.is_active = bool(data['is_active'])
    
    if 'is_featured' in data:
        link.is_featured = bool(data['is_featured'])
    
    if 'display_order' in data:
        link.display_order = data['display_order']
    
    if 'link_type' in data:
        link.link_type = data['link_type']
    
    if 'reference_id' in data:
        link.reference_id = data['reference_id']
    
    if 'settings' in data:
        link.set_settings(data['settings'])
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': link.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/links/<int:link_id>', methods=['DELETE'])
@login_required
def delete_link(link_id):
    """API endpoint to delete a link"""
    link = Link.query.filter_by(id=link_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(link)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/links/reorder', methods=['POST'])
@login_required
def reorder_links():
    """API endpoint to reorder links"""
    data = request.get_json()
    
    if not data or 'links' not in data:
        return jsonify({'error': 'Missing links data'}), 400
    
    try:
        for item in data['links']:
            link_id = item.get('id')
            display_order = item.get('display_order')
            
            if link_id and display_order is not None:
                link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
                if link:
                    link.display_order = display_order
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/menus/add-to-profile', methods=['POST'])
@login_required
def add_menu_to_profile():
    """API endpoint to add a menu to user profile as a link"""
    data = request.get_json()
    
    if not data or 'menu_id' not in data:
        return jsonify({'error': 'Missing menu_id'}), 400
    
    menu_id = data.get('menu_id')
    
    # Verify menu exists and belongs to user
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).first_or_404()
    
    # Create link for menu
    try:
        link = Link(
            title=f"{menu.name} Menu",
            url=menu.get_full_url(),
            user_id=current_user.id,
            description=menu.description,
            icon='utensils',  # Font Awesome icon for food
            category='Menu',
            is_featured=data.get('is_featured', False),
            display_order=data.get('display_order', 0),
            link_type='menu',
            reference_id=menu.id
        )
        
        db.session.add(link)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': link.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/shorturls/add-to-profile', methods=['POST'])
@login_required
def add_shorturl_to_profile():
    """API endpoint to add a short URL to user profile as a link"""
    data = request.get_json()
    
    if not data or 'shorturl_id' not in data:
        return jsonify({'error': 'Missing shorturl_id'}), 400
    
    shorturl_id = data.get('shorturl_id')
    
    # Verify short URL exists and belongs to user
    shorturl = ShortURL.query.filter_by(id=shorturl_id, user_id=current_user.id).first_or_404()
    
    # Create link for short URL
    try:
        link = Link(
            title=data.get('title', 'Shortened URL'),
            url=shorturl.get_full_shortened_url(),
            user_id=current_user.id,
            description=f"Shortened link for: {shorturl.original_url[:50]}...",
            icon='link',  # Font Awesome icon for link
            category='Short URL',
            is_featured=data.get('is_featured', False),
            display_order=data.get('display_order', 0),
            link_type='shorturl',
            reference_id=shorturl.id
        )
        
        db.session.add(link)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': link.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<username>', methods=['GET'])
def view_profile(username):
    """Public endpoint to view a user's profile"""
    user = User.query.filter_by(username=username, is_active=True).first_or_404()
    
    # Get active links ordered by display_order
    links = Link.query.filter_by(user_id=user.id, is_active=True).order_by(Link.display_order).all()
    
    # Get featured links
    featured_links = [link for link in links if link.is_featured]
    
    # Group links by category
    categorized_links = {}
    for link in links:
        category = link.category or 'Other'
        if category not in categorized_links:
            categorized_links[category] = []
        categorized_links[category].append(link)
    
    return render_template('profile/view.html', 
                          user=user, 
                          links=links, 
                          featured_links=featured_links, 
                          categorized_links=categorized_links)

@user_bp.route('/l/<username>/<int:link_id>', methods=['GET'])
def redirect_link(username, link_id):
    """Redirect to a link and track click"""
    link = Link.query.join(User).filter(
        Link.id == link_id,
        User.username == username,
        Link.is_active == True,
        User.is_active == True
    ).first_or_404()
    
    # Increment click count
    link.increment_click()
    
    # Redirect to the URL
    return redirect(link.url)

@user_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Dashboard home page"""
    return render_template('dashboard/index.html')

@user_bp.route('/dashboard/links', methods=['GET'])
@login_required
def links_dashboard():
    """Dashboard page for managing links"""
    return render_template('dashboard/links.html')

@user_bp.route('/dashboard/profile', methods=['GET'])
@login_required
def profile_dashboard():
    """Dashboard page for managing profile"""
    return render_template('dashboard/profile.html')
