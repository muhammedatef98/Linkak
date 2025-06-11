from flask import Blueprint, request, render_template, jsonify, abort, url_for, current_app
from src.models.menu import Menu, MenuCategory, MenuItem, db
from flask_login import login_required, current_user
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/api/menus', methods=['GET'])
@login_required
def get_user_menus():
    """API endpoint to get user's menus"""
    menus = Menu.query.filter_by(user_id=current_user.id).order_by(Menu.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [menu.to_dict() for menu in menus]
    })

@menu_bp.route('/api/menus', methods=['POST'])
@login_required
def create_menu():
    """API endpoint to create a new menu"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'business_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create new menu
    try:
        menu = Menu(
            name=data.get('name'),
            user_id=current_user.id,
            business_name=data.get('business_name'),
            description=data.get('description'),
            business_logo=data.get('business_logo'),
            theme=data.get('theme', 'default'),
            custom_url=data.get('custom_url')
        )
        db.session.add(menu)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': menu.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/menus/<int:menu_id>', methods=['GET'])
@login_required
def get_menu(menu_id):
    """API endpoint to get a specific menu"""
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).first_or_404()
    return jsonify({
        'success': True,
        'data': menu.to_dict()
    })

@menu_bp.route('/api/menus/<int:menu_id>', methods=['PUT'])
@login_required
def update_menu(menu_id):
    """API endpoint to update a menu"""
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).first_or_404()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'name' in data:
        menu.name = data['name']
    
    if 'business_name' in data:
        menu.business_name = data['business_name']
    
    if 'description' in data:
        menu.description = data['description']
    
    if 'business_logo' in data:
        menu.business_logo = data['business_logo']
    
    if 'theme' in data:
        menu.theme = data['theme']
    
    if 'is_published' in data:
        menu.is_published = bool(data['is_published'])
    
    if 'custom_url' in data:
        menu.custom_url = data['custom_url']
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': menu.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/menus/<int:menu_id>', methods=['DELETE'])
@login_required
def delete_menu(menu_id):
    """API endpoint to delete a menu"""
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(menu)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/menus/<int:menu_id>/categories', methods=['POST'])
@login_required
def create_category(menu_id):
    """API endpoint to create a new menu category"""
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).first_or_404()
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create new category
    try:
        category = MenuCategory(
            name=data.get('name'),
            menu_id=menu.id,
            description=data.get('description'),
            display_order=data.get('display_order', 0)
        )
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/categories/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    """API endpoint to update a menu category"""
    category = MenuCategory.query.join(Menu).filter(
        MenuCategory.id == category_id,
        Menu.user_id == current_user.id
    ).first_or_404()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'name' in data:
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    
    if 'display_order' in data:
        category.display_order = data['display_order']
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': category.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """API endpoint to delete a menu category"""
    category = MenuCategory.query.join(Menu).filter(
        MenuCategory.id == category_id,
        Menu.user_id == current_user.id
    ).first_or_404()
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/categories/<int:category_id>/items', methods=['POST'])
@login_required
def create_item(category_id):
    """API endpoint to create a new menu item"""
    category = MenuCategory.query.join(Menu).filter(
        MenuCategory.id == category_id,
        Menu.user_id == current_user.id
    ).first_or_404()
    
    # Handle form data with file upload
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        image_file = request.files.get('image')
        
        # Save image if provided
        image_path = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Create directory if it doesn't exist
            upload_dir = os.path.join(current_app.static_folder, 'uploads', 'menu_items')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, filename)
            image_file.save(file_path)
            
            # Store relative path
            image_path = f"/static/uploads/menu_items/{filename}"
        
        # Parse options if provided
        options = None
        if 'options' in data:
            try:
                options = json.loads(data['options'])
            except json.JSONDecodeError:
                options = None
    else:
        # Handle JSON data
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        image_path = data.get('image')
        options = data.get('options')
    
    # Create new item
    try:
        item = MenuItem(
            name=data.get('name'),
            category_id=category.id,
            description=data.get('description'),
            price=float(data.get('price')) if data.get('price') else None,
            image=image_path,
            is_available=bool(int(data.get('is_available', 1))),
            is_featured=bool(int(data.get('is_featured', 0))),
            display_order=int(data.get('display_order', 0)),
            options=options
        )
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/items/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    """API endpoint to update a menu item"""
    item = MenuItem.query.join(MenuCategory, Menu).filter(
        MenuItem.id == item_id,
        Menu.user_id == current_user.id
    ).first_or_404()
    
    # Handle form data with file upload
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        image_file = request.files.get('image')
        
        # Save image if provided
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Create directory if it doesn't exist
            upload_dir = os.path.join(current_app.static_folder, 'uploads', 'menu_items')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, filename)
            image_file.save(file_path)
            
            # Store relative path
            item.image = f"/static/uploads/menu_items/{filename}"
        
        # Parse options if provided
        if 'options' in data:
            try:
                item.options = json.dumps(json.loads(data['options']))
            except json.JSONDecodeError:
                pass
    else:
        # Handle JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'image' in data:
            item.image = data['image']
        
        if 'options' in data:
            item.options = json.dumps(data['options']) if data['options'] else None
    
    # Update fields
    if 'name' in data:
        item.name = data['name']
    
    if 'description' in data:
        item.description = data['description']
    
    if 'price' in data and data['price']:
        item.price = float(data['price'])
    
    if 'is_available' in data:
        item.is_available = bool(int(data['is_available']))
    
    if 'is_featured' in data:
        item.is_featured = bool(int(data['is_featured']))
    
    if 'display_order' in data:
        item.display_order = int(data['display_order'])
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'data': item.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    """API endpoint to delete a menu item"""
    item = MenuItem.query.join(MenuCategory, Menu).filter(
        MenuItem.id == item_id,
        Menu.user_id == current_user.id
    ).first_or_404()
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/menu/<custom_url>', methods=['GET'])
def view_menu_by_custom_url(custom_url):
    """Public endpoint to view a menu by custom URL"""
    menu = Menu.query.filter_by(custom_url=custom_url, is_published=True).first_or_404()
    return render_template('menu/view.html', menu=menu)

@menu_bp.route('/menu/<int:menu_id>', methods=['GET'])
def view_menu(menu_id):
    """Public endpoint to view a menu by ID"""
    menu = Menu.query.filter_by(id=menu_id, is_published=True).first_or_404()
    return render_template('menu/view.html', menu=menu)

@menu_bp.route('/dashboard/menus', methods=['GET'])
@login_required
def menu_dashboard():
    """Dashboard page for managing menus"""
    return render_template('dashboard/menus.html')

@menu_bp.route('/dashboard/menus/<int:menu_id>/edit', methods=['GET'])
@login_required
def edit_menu(menu_id):
    """Dashboard page for editing a specific menu"""
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).first_or_404()
    return render_template('dashboard/menu_edit.html', menu=menu)
