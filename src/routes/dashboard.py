from flask import Blueprint, send_from_directory, session, redirect, url_for
import os

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    dashboard_path = os.path.join(static_folder, 'dashboard', 'index.html')
    
    if os.path.exists(dashboard_path):
        return send_from_directory(os.path.join(static_folder, 'dashboard'), 'index.html')
    else:
        return "Dashboard not found", 404
