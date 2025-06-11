#!/bin/bash

# Create requirements.txt file
echo "Creating requirements.txt file..."
cat > /home/ubuntu/Linkak/requirements.txt << 'EOF'
flask==2.0.1
flask-login==0.5.0
flask-sqlalchemy==2.5.1
werkzeug==2.0.1
validators==0.18.2
qrcode==7.3.1
pillow==8.3.1
gunicorn==20.1.0
pymysql==1.0.2
EOF

# Create a README file
echo "Creating README.md file..."
cat > /home/ubuntu/Linkak/README.md << 'EOF'
# Linkak - Your Professional Digital Identity Hub

Linkak is a modern, full-stack web application that allows users to create a centralized hub for all their professional and personal links. Unlike similar platforms, Linkak offers enhanced features focused on professional branding, analytics, and customization.

## Key Features

- **Professional Branding Focus** - Custom domain integration, industry-specific templates, and resume/CV integration
- **Enhanced Analytics** - Detailed visitor demographics, heat maps, and conversion tracking
- **Advanced Customization** - Full CSS control, interactive elements, and animation options
- **Monetization Options** - Built-in tipping system, product showcase, and affiliate link tracking
- **SEO & Discoverability** - Built-in SEO tools and public directory
- **Security & Privacy** - Granular privacy controls and scheduled link visibility
- **Collaboration Features** - Team accounts and role-based permissions
- **Integration Ecosystem** - API for third-party integrations
- **URL Shortening** - Free custom domain URL shortening with analytics
- **Business Menu Builder** - Create digital menus for restaurants and businesses

## Getting Started

Please refer to the following documentation:

- [Full Documentation](DOCUMENTATION.md) - Comprehensive guide to all features and configuration
- [GitHub Instructions](GITHUB_INSTRUCTIONS.md) - How to upload and manage this project on GitHub
- [Mac Setup Guide](MAC_SETUP_GUIDE.md) - Specific instructions for Mac users

## Quick Start

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python -m src.main`
6. Access at http://localhost:5000

## License

This project is licensed under the MIT License - see the LICENSE file for details.
EOF

# Create a simple license file
echo "Creating LICENSE file..."
cat > /home/ubuntu/Linkak/LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Linkak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create a .gitignore file
echo "Creating .gitignore file..."
cat > /home/ubuntu/Linkak/.gitignore << 'EOF'
# Python virtual environment
venv/
env/
ENV/

# Python cache files
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Database files
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.*

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Log files
*.log
logs/

# Temporary files
tmp/
temp/
EOF

# Create directories for static files if they don't exist
mkdir -p /home/ubuntu/Linkak/src/static/uploads/profiles
mkdir -p /home/ubuntu/Linkak/src/static/uploads/menu_items
mkdir -p /home/ubuntu/Linkak/src/static/qrcodes

echo "Package preparation complete!"
