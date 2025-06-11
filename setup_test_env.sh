#!/bin/bash

# Create necessary directories for static assets
mkdir -p /home/ubuntu/LinkHub/src/static/img

# Create placeholder images
echo "Creating placeholder images..."
cat > /home/ubuntu/LinkHub/src/static/img/hero-image.svg << 'EOF'
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f0f4f8"/>
  <text x="50%" y="50%" font-family="Arial" font-size="24" fill="#4f46e5" text-anchor="middle">LinkHub Preview</text>
  <rect x="100" y="100" width="400" height="60" rx="10" fill="#4f46e5" opacity="0.8"/>
  <rect x="100" y="180" width="400" height="60" rx="10" fill="#4f46e5" opacity="0.6"/>
  <rect x="100" y="260" width="400" height="60" rx="10" fill="#4f46e5" opacity="0.4"/>
</svg>
EOF

cat > /home/ubuntu/LinkHub/src/static/img/testimonial-1.jpg << 'EOF'
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#e2e8f0"/>
  <circle cx="100" cy="100" r="70" fill="#94a3b8"/>
  <circle cx="100" cy="80" r="30" fill="#cbd5e1"/>
  <path d="M100 120 Q100 180 150 160 Q50 180 100 120" fill="#cbd5e1"/>
</svg>
EOF

# Enable database in main.py
sed -i 's/# app.config/app.config/g' /home/ubuntu/LinkHub/src/main.py
sed -i 's/# db.init_app/db.init_app/g' /home/ubuntu/LinkHub/src/main.py
sed -i 's/# with app.app_context/with app.app_context/g' /home/ubuntu/LinkHub/src/main.py
sed -i 's/#     db.create_all/    db.create_all/g' /home/ubuntu/LinkHub/src/main.py

# Create dashboard template
mkdir -p /home/ubuntu/LinkHub/src/static/dashboard

cat > /home/ubuntu/LinkHub/src/static/dashboard/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkHub Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="/static/dashboard/dashboard.css">
    <script src="/static/dashboard/dashboard.js" defer></script>
</head>
<body class="dashboard-body">
    <div class="dashboard-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>LinkHub</h2>
            </div>
            <nav class="sidebar-nav">
                <ul>
                    <li class="active"><a href="#"><i class="fas fa-home"></i> Dashboard</a></li>
                    <li><a href="#"><i class="fas fa-link"></i> My Links</a></li>
                    <li><a href="#"><i class="fas fa-chart-line"></i> Analytics</a></li>
                    <li><a href="#"><i class="fas fa-paint-brush"></i> Appearance</a></li>
                    <li><a href="#"><i class="fas fa-cog"></i> Settings</a></li>
                </ul>
            </nav>
            <div class="sidebar-footer">
                <a href="#" id="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </aside>
        
        <main class="main-content">
            <header class="dashboard-header">
                <div class="search-bar">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search...">
                </div>
                <div class="user-menu">
                    <span class="username">Welcome, <span id="user-name">User</span></span>
                    <div class="profile-image">
                        <img src="/static/img/testimonial-1.jpg" alt="Profile">
                    </div>
                </div>
            </header>
            
            <div class="dashboard-content">
                <div class="page-header">
                    <h1>Dashboard</h1>
                    <button class="btn-primary"><i class="fas fa-plus"></i> Add New Link</button>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-eye"></i>
                        </div>
                        <div class="stat-content">
                            <h3>Total Views</h3>
                            <p class="stat-value">1,234</p>
                            <p class="stat-change positive">+12% from last week</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-mouse-pointer"></i>
                        </div>
                        <div class="stat-content">
                            <h3>Total Clicks</h3>
                            <p class="stat-value">567</p>
                            <p class="stat-change positive">+8% from last week</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-link"></i>
                        </div>
                        <div class="stat-content">
                            <h3>Active Links</h3>
                            <p class="stat-value">12</p>
                            <p class="stat-change neutral">No change</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-dollar-sign"></i>
                        </div>
                        <div class="stat-content">
                            <h3>Revenue</h3>
                            <p class="stat-value">$25.40</p>
                            <p class="stat-change positive">+15% from last week</p>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2>Top Performing Links</h2>
                            <a href="#" class="card-action">View All</a>
                        </div>
                        <div class="card-content">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Link</th>
                                        <th>Clicks</th>
                                        <th>CTR</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>My Portfolio</td>
                                        <td>245</td>
                                        <td>24.5%</td>
                                    </tr>
                                    <tr>
                                        <td>GitHub Profile</td>
                                        <td>189</td>
                                        <td>18.9%</td>
                                    </tr>
                                    <tr>
                                        <td>LinkedIn</td>
                                        <td>132</td>
                                        <td>13.2%</td>
                                    </tr>
                                    <tr>
                                        <td>Twitter</td>
                                        <td>87</td>
                                        <td>8.7%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2>Visitor Demographics</h2>
                            <a href="#" class="card-action">View Details</a>
                        </div>
                        <div class="card-content">
                            <div class="chart-container">
                                <div class="chart-placeholder">
                                    <div class="chart-bar" style="height: 70%;"></div>
                                    <div class="chart-bar" style="height: 90%;"></div>
                                    <div class="chart-bar" style="height: 50%;"></div>
                                    <div class="chart-bar" style="height: 65%;"></div>
                                    <div class="chart-bar" style="height: 40%;"></div>
                                </div>
                                <div class="chart-labels">
                                    <span>USA</span>
                                    <span>UK</span>
                                    <span>Canada</span>
                                    <span>Germany</span>
                                    <span>Others</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-card full-width">
                    <div class="card-header">
                        <h2>Recent Activity</h2>
                        <a href="#" class="card-action">View All</a>
                    </div>
                    <div class="card-content">
                        <ul class="activity-list">
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-plus"></i>
                                </div>
                                <div class="activity-content">
                                    <p>Added new link: <strong>My Blog</strong></p>
                                    <span class="activity-time">2 hours ago</span>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-edit"></i>
                                </div>
                                <div class="activity-content">
                                    <p>Updated profile information</p>
                                    <span class="activity-time">Yesterday</span>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-trash"></i>
                                </div>
                                <div class="activity-content">
                                    <p>Deleted link: <strong>Old Project</strong></p>
                                    <span class="activity-time">3 days ago</span>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-paint-brush"></i>
                                </div>
                                <div class="activity-content">
                                    <p>Changed theme to <strong>Professional Dark</strong></p>
                                    <span class="activity-time">1 week ago</span>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
EOF

# Create dashboard CSS
cat > /home/ubuntu/LinkHub/src/static/dashboard/dashboard.css << 'EOF'
/* Dashboard Styles */
.dashboard-body {
    background-color: var(--gray-100);
}

.dashboard-container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 250px;
    background-color: var(--gray-900);
    color: white;
    display: flex;
    flex-direction: column;
    position: fixed;
    height: 100vh;
}

.sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--gray-800);
}

.sidebar-header h2 {
    color: var(--primary-color);
    margin: 0;
}

.sidebar-nav {
    flex: 1;
    padding: 1.5rem 0;
}

.sidebar-nav ul li {
    margin-bottom: 0.5rem;
}

.sidebar-nav ul li a {
    display: flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    color: var(--gray-400);
    transition: var(--transition);
}

.sidebar-nav ul li a:hover,
.sidebar-nav ul li.active a {
    color: white;
    background-color: var(--gray-800);
}

.sidebar-nav ul li a i {
    margin-right: 0.75rem;
    width: 20px;
    text-align: center;
}

.sidebar-footer {
    padding: 1.5rem;
    border-top: 1px solid var(--gray-800);
}

.sidebar-footer a {
    color: var(--gray-400);
    display: flex;
    align-items: center;
}

.sidebar-footer a:hover {
    color: white;
}

.sidebar-footer a i {
    margin-right: 0.75rem;
}

/* Main Content */
.main-content {
    flex: 1;
    margin-left: 250px;
}

.dashboard-header {
    background-color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-bar {
    display: flex;
    align-items: center;
    background-color: var(--gray-100);
    border-radius: var(--border-radius);
    padding: 0.5rem 1rem;
    width: 300px;
}

.search-bar i {
    color: var(--gray-500);
    margin-right: 0.5rem;
}

.search-bar input {
    border: none;
    background: transparent;
    width: 100%;
    font-size: 0.9rem;
}

.search-bar input:focus {
    outline: none;
}

.user-menu {
    display: flex;
    align-items: center;
}

.username {
    margin-right: 1rem;
    color: var(--gray-700);
}

.profile-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
}

.profile-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Dashboard Content */
.dashboard-content {
    padding: 2rem;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.page-header h1 {
    color: var(--gray-900);
    margin: 0;
}

.page-header .btn-primary i {
    margin-right: 0.5rem;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 1.5rem;
    display: flex;
    align-items: center;
    box-shadow: var(--box-shadow);
}

.stat-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--primary-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    margin-right: 1rem;
}

.stat-content h3 {
    font-size: 0.9rem;
    color: var(--gray-600);
    margin: 0 0 0.5rem;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gray-900);
    margin: 0 0 0.25rem;
}

.stat-change {
    font-size: 0.8rem;
    margin: 0;
}

.stat-change.positive {
    color: var(--success-color);
}

.stat-change.negative {
    color: var(--danger-color);
}

.stat-change.neutral {
    color: var(--gray-500);
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.dashboard-card {
    background-color: white;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    overflow: hidden;
}

.dashboard-card.full-width {
    grid-column: 1 / -1;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--gray-200);
}

.card-header h2 {
    font-size: 1.1rem;
    color: var(--gray-900);
    margin: 0;
}

.card-action {
    font-size: 0.9rem;
    color: var(--primary-color);
}

.card-content {
    padding: 1.5rem;
}

/* Data Table */
.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 0.75rem;
    text-align: left;
}

.data-table th {
    font-weight: 600;
    color: var(--gray-700);
    border-bottom: 1px solid var(--gray-300);
}

.data-table td {
    color: var(--gray-800);
    border-bottom: 1px solid var(--gray-200);
}

.data-table tr:last-child td {
    border-bottom: none;
}

/* Chart */
.chart-container {
    height: 200px;
    display: flex;
    flex-direction: column;
}

.chart-placeholder {
    flex: 1;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    padding: 0 1rem;
    margin-bottom: 1rem;
}

.chart-bar {
    width: 40px;
    background: linear-gradient(to top, var(--primary-color), var(--primary-hover));
    border-radius: 4px 4px 0 0;
}

.chart-labels {
    display: flex;
    justify-content: space-around;
}

.chart-labels span {
    font-size: 0.8rem;
    color: var(--gray-600);
    text-align: center;
    width: 60px;
}

/* Activity List */
.activity-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.activity-item {
    display: flex;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid var(--gray-200);
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: var(--primary-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
}

.activity-content p {
    margin: 0 0 0.25rem;
    color: var(--gray-800);
}

.activity-time {
    font-size: 0.8rem;
    color: var(--gray-500);
}

/* Responsive */
@media (max-width: 992px) {
    .sidebar {
        width: 70px;
    }
    
    .sidebar-header h2,
    .sidebar-nav ul li a span,
    .sidebar-footer a span {
        display: none;
    }
    
    .sidebar-nav ul li a {
        justify-content: center;
        padding: 0.75rem;
    }
    
    .sidebar-nav ul li a i {
        margin-right: 0;
    }
    
    .sidebar-footer a {
        justify-content: center;
    }
    
    .sidebar-footer a i {
        margin-right: 0;
    }
    
    .main-content {
        margin-left: 70px;
    }
}

@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .search-bar {
        width: 200px;
    }
}

@media (max-width: 576px) {
    .dashboard-header {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
    }
    
    .search-bar {
        width: 100%;
    }
    
    .user-menu {
        justify-content: space-between;
    }
    
    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
EOF

# Create dashboard JavaScript
cat > /home/ubuntu/LinkHub/src/static/dashboard/dashboard.js << 'EOF'
document.addEventListener('DOMContentLoaded', function() {
    // Fetch user data
    fetch('/api/profile')
        .then(response => {
            if (!response.ok) {
                // If not authenticated, redirect to login
                if (response.status === 401) {
                    window.location.href = '/';
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update user name
            const userName = document.getElementById('user-name');
            if (userName && data.user && data.user.full_name) {
                userName.textContent = data.user.full_name;
            } else if (userName && data.user && data.user.username) {
                userName.textContent = data.user.username;
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
    
    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                window.location.href = '/';
            })
            .catch(error => {
                console.error('Error logging out:', error);
            });
        });
    }
    
    // Sidebar navigation
    const navItems = document.querySelectorAll('.sidebar-nav ul li');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
EOF

# Create a route for the dashboard
cat > /home/ubuntu/LinkHub/src/routes/dashboard.py << 'EOF'
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
EOF

# Update main.py to include the dashboard blueprint
sed -i "/from src.routes.user import user_bp/a from src.routes.dashboard import dashboard_bp" /home/ubuntu/LinkHub/src/main.py
sed -i "/app.register_blueprint(user_bp, url_prefix='\/api')/a app.register_blueprint(dashboard_bp)" /home/ubuntu/LinkHub/src/main.py

# Create a test script
cat > /home/ubuntu/LinkHub/test.py << 'EOF'
import requests
import json
import sys
import time

def test_api(base_url):
    print("Testing LinkHub API...")
    
    # Test registration
    print("\n1. Testing user registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/register", json=register_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Registration test passed")
        else:
            print("❌ Registration test failed")
    except Exception as e:
        print(f"❌ Registration test error: {str(e)}")
    
    # Test login
    print("\n2. Testing user login...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Login test passed")
            cookies = response.cookies
        else:
            print("❌ Login test failed")
            cookies = None
    except Exception as e:
        print(f"❌ Login test error: {str(e)}")
        cookies = None
    
    # Test profile retrieval
    if cookies:
        print("\n3. Testing profile retrieval...")
        try:
            response = requests.get(f"{base_url}/api/profile", cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Profile retrieval test passed")
            else:
                print("❌ Profile retrieval test failed")
        except Exception as e:
            print(f"❌ Profile retrieval test error: {str(e)}")
        
        # Test link creation
        print("\n4. Testing link creation...")
        link_data = {
            "title": "Test Link",
            "url": "https://example.com",
            "description": "This is a test link"
        }
        
        try:
            response = requests.post(f"{base_url}/api/links", json=link_data, cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                print("✅ Link creation test passed")
                link_id = response.json().get('link', {}).get('id')
            else:
                print("❌ Link creation test failed")
                link_id = None
        except Exception as e:
            print(f"❌ Link creation test error: {str(e)}")
            link_id = None
        
        # Test link retrieval
        print("\n5. Testing link retrieval...")
        try:
            response = requests.get(f"{base_url}/api/links", cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Link retrieval test passed")
            else:
                print("❌ Link retrieval test failed")
        except Exception as e:
            print(f"❌ Link retrieval test error: {str(e)}")
        
        # Test link update
        if link_id:
            print("\n6. Testing link update...")
            update_data = {
                "title": "Updated Test Link",
                "description": "This is an updated test link"
            }
            
            try:
                response = requests.put(f"{base_url}/api/links/{link_id}", json=update_data, cookies=cookies)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Link update test passed")
                else:
                    print("❌ Link update test failed")
            except Exception as e:
                print(f"❌ Link update test error: {str(e)}")
            
            # Test link deletion
            print("\n7. Testing link deletion...")
            try:
                response = requests.delete(f"{base_url}/api/links/{link_id}", cookies=cookies)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Link deletion test passed")
                else:
                    print("❌ Link deletion test failed")
            except Exception as e:
                print(f"❌ Link deletion test error: {str(e)}")
        
        # Test logout
        print("\n8. Testing user logout...")
        try:
            response = requests.post(f"{base_url}/api/logout", cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Logout test passed")
            else:
                print("❌ Logout test failed")
        except Exception as e:
            print(f"❌ Logout test error: {str(e)}")
    
    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    test_api(base_url)
EOF

# Create a setup and run guide
cat > /home/ubuntu/LinkHub/SETUP_AND_RUN.md << 'EOF'
# LinkHub Setup and Run Guide

This guide will walk you through setting up and running the LinkHub application from scratch.

## Prerequisites

- Python 3.6 or higher
- MySQL (optional, for production)
- Git (optional, for version control)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/LinkHub.git
cd LinkHub
```

Or download and extract the ZIP file.

## Step 2: Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Database (Optional)

By default, LinkHub uses SQLite for development. For production, you can use MySQL:

1. Uncomment the database configuration in `src/main.py`
2. Set up environment variables for your database:
   - `DB_USERNAME` (default: root)
   - `DB_PASSWORD` (default: password)
   - `DB_HOST` (default: localhost)
   - `DB_PORT` (default: 3306)
   - `DB_NAME` (default: mydb)

## Step 5: Run the Application

```bash
# Make sure you're in the project root directory
cd /path/to/LinkHub

# Activate the virtual environment if not already activated
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Run the application
python -m src.main
```

The application will be available at http://localhost:5000

## Step 6: Access the Application

- Landing page: http://localhost:5000
- Dashboard (after login): http://localhost:5000/dashboard

## Step 7: Testing the API

You can test the API using the included test script:

```bash
python test.py http://localhost:5000
```

## Production Deployment

For production deployment, consider:

1. Using a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. Setting up a reverse proxy with Nginx or Apache

3. Using a production database (MySQL or PostgreSQL)

4. Setting proper environment variables for security:
   - Set a strong `SECRET_KEY` in `src/main.py`
   - Configure database credentials securely

## API Documentation

### Authentication

- `POST /api/register` - Register a new user
- `POST /api/login` - Log in a user
- `POST /api/logout` - Log out a user

### Profile Management

- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Link Management

- `GET /api/links` - Get all links for the logged-in user
- `POST /api/links` - Create a new link
- `PUT /api/links/<link_id>` - Update a link
- `DELETE /api/links/<link_id>` - Delete a link

### Analytics

- `GET /api/analytics` - Get analytics data for the logged-in user

## Troubleshooting

- **Database Connection Issues**: Verify your database credentials and ensure the database server is running
- **Import Errors**: Make sure you're running the application from the project root directory
- **Permission Errors**: Ensure you have write permissions for the application directory

## Support

For support, please open an issue on the GitHub repository or contact the maintainer.
EOF

echo "Test and validation setup complete!"
