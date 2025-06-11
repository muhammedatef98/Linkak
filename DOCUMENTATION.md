# Linkak Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Deployment](#deployment)
8. [GitHub Upload Instructions](#github-upload-instructions)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

## Introduction

Linkak is a professional digital identity hub that allows users to create a centralized location for all their professional and personal links. Unlike similar platforms like Linktree, Linkak offers enhanced features focused on professional branding, analytics, and customization.

### What Makes Linkak Unique

Linkak stands out with its comprehensive feature set designed for professionals and businesses:

- **Free custom domain URL shortening** - Create branded short links using your own domain
- **Business menu builder** - Create digital menus for restaurants and businesses
- **Advanced analytics** - Get detailed insights about your visitors and link performance
- **AI-powered recommendations** - Receive intelligent suggestions to optimize your profile
- **Scheduled content** - Plan content changes in advance with time-based activation
- **Team collaboration** - Work together with colleagues on shared profiles and resources

## Features

### Core Features

#### Professional Branding Focus
- Custom domain integration without premium subscription
- Industry-specific templates designed for different industries
- Resume/CV integration option for professional profiles
- LinkedIn-style endorsements for links and skills

#### Enhanced Analytics
- Detailed visitor demographics and behavior tracking
- Heat maps showing which links get the most attention
- Conversion tracking for business-oriented links
- A/B testing capabilities for link placement and descriptions

#### Advanced Customization
- Full CSS control for developers
- Interactive elements (polls, forms, mini-apps)
- Seasonal themes and automatic day/night mode
- Animation options for links and page elements

#### Monetization Options
- Built-in tipping/donation system
- Product showcase with direct purchase options
- Affiliate link integration and tracking
- Subscription content gating

#### SEO & Discoverability
- Built-in SEO optimization tools
- Public directory of Linkak profiles (opt-in)
- Tag-based discovery system
- Integration with search engines

#### Security & Privacy
- Granular privacy controls for each link
- Scheduled link visibility (time-based access)
- Geographic restrictions option
- Password-protected sections

#### Collaboration Features
- Team accounts for businesses and groups
- Collaborative editing of shared profiles
- Role-based permissions
- Activity logs and change history

#### Integration Ecosystem
- API for third-party integrations
- Webhook support for automated updates
- Social media cross-posting
- Calendar/event integration

### Unique Features

#### URL Shortening
- Free custom domain URL shortening
- Analytics for shortened links
- QR code generation for each shortened URL
- Custom alias support

#### Business Menu Builder
- Create digital menus for restaurants and businesses
- Customizable menu categories and items
- Price and description management
- Seamless integration with your profile links

#### AI Recommendations
- Layout optimization suggestions
- Content improvement recommendations
- Theme and style suggestions
- Performance insights based on visitor behavior

#### Advanced Analytics Dashboard
- Comprehensive visitor demographics
- Engagement metrics and trends
- Conversion tracking
- Geographic and device breakdowns

#### Scheduled Content Management
- Time-based content activation/deactivation
- Seasonal promotions scheduling
- Limited-time offers automation
- Content rotation capabilities

#### Team Collaboration Tools
- Shared profile management
- Role-based permissions
- Activity tracking
- Collaborative editing features

## Installation

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)
- SQLite (default) or MySQL (for production)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/linkak.git
   cd linkak
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python -m src.main
   ```

5. **Run the application**
   ```bash
   python -m src.main
   ```

6. **Access the application**
   Open your browser and navigate to http://localhost:5000

## Configuration

### Environment Variables

Linkak supports the following environment variables for configuration:

- `SECRET_KEY`: Secret key for session security (required for production)
- `SQLALCHEMY_DATABASE_URI`: Database connection string (defaults to SQLite)
- `DEBUG`: Enable debug mode (set to False in production)
- `PORT`: Port to run the application on (defaults to 5000)
- `HOST`: Host to bind the application to (defaults to 0.0.0.0)

### Database Configuration

By default, Linkak uses SQLite for development. For production, it's recommended to use MySQL:

```python
# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'linkak')}"
```

## Usage Guide

### Creating Your Profile

1. **Register an account**
   - Navigate to the registration page
   - Enter your username, email, and password
   - Click "Register"

2. **Set up your profile**
   - Add your name, bio, and profile picture
   - Choose a theme for your profile
   - Configure your profile settings

3. **Add links**
   - Click "Add Link" in your dashboard
   - Enter the title, URL, and description
   - Choose an icon or upload a custom image
   - Set the category and display order
   - Toggle featured status if desired

### Using URL Shortener

1. **Create a shortened URL**
   - Navigate to the URL Shortener section
   - Enter the original URL
   - Optionally set a custom alias
   - Choose a custom domain (if available)
   - Click "Shorten"

2. **View analytics**
   - See click counts and visitor data
   - Analyze geographic and device information
   - Track referrers and conversion rates

3. **Add to your profile**
   - Click "Add to Profile" on any shortened URL
   - Customize the title and appearance
   - Set the display order and category

### Creating Business Menus

1. **Create a new menu**
   - Navigate to the Menu Builder section
   - Enter your business name and menu title
   - Add a description and choose a theme
   - Click "Create Menu"

2. **Add categories**
   - Click "Add Category"
   - Enter the category name and description
   - Set the display order
   - Click "Save"

3. **Add menu items**
   - Select a category
   - Click "Add Item"
   - Enter the item name, description, and price
   - Upload an image (optional)
   - Add options or variations (optional)
   - Click "Save"

4. **Add to your profile**
   - Click "Add to Profile" on any menu
   - Customize the title and appearance
   - Set the display order and category

### Using Advanced Features

#### AI Recommendations

1. **Generate recommendations**
   - Navigate to the AI Recommendations section
   - Click "Generate Recommendations"
   - Choose the type of recommendations (layout, content, theme)
   - Review the suggestions

2. **Apply recommendations**
   - Review each recommendation
   - Click "Apply" to implement the changes
   - Customize as needed

#### Scheduled Content

1. **Create scheduled content**
   - Navigate to the Scheduled Content section
   - Choose the content type (link, theme, profile)
   - Select the action (activate, deactivate, update)
   - Set the scheduled time
   - Click "Schedule"

2. **Manage scheduled content**
   - View all scheduled items
   - Edit or delete scheduled items
   - Monitor execution status

#### Team Collaboration

1. **Invite collaborators**
   - Navigate to the Collaboration section
   - Enter the collaborator's email
   - Choose the resource to share
   - Set permission level
   - Click "Invite"

2. **Manage collaborations**
   - View all collaborations
   - Change permission levels
   - Remove collaborators

## API Reference

Linkak provides a comprehensive API for integrating with other services.

### Authentication

All API requests require authentication using a bearer token:

```
Authorization: Bearer YOUR_API_TOKEN
```

### Endpoints

#### User API

- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile
- `POST /api/profile/image` - Update profile image

#### Links API

- `GET /api/links` - Get user's links
- `POST /api/links` - Create a new link
- `PUT /api/links/:id` - Update a link
- `DELETE /api/links/:id` - Delete a link
- `POST /api/links/reorder` - Reorder links

#### URL Shortener API

- `POST /api/shorten` - Create a shortened URL
- `GET /api/urls` - Get user's shortened URLs
- `GET /api/urls/:id` - Get details of a specific shortened URL
- `PUT /api/urls/:id` - Update a shortened URL
- `DELETE /api/urls/:id` - Delete a shortened URL
- `GET /api/qrcode/:short_code` - Get QR code for a shortened URL

#### Menu Builder API

- `GET /api/menus` - Get user's menus
- `POST /api/menus` - Create a new menu
- `GET /api/menus/:id` - Get a specific menu
- `PUT /api/menus/:id` - Update a menu
- `DELETE /api/menus/:id` - Delete a menu
- `POST /api/menus/:id/categories` - Create a new menu category
- `PUT /api/categories/:id` - Update a menu category
- `DELETE /api/categories/:id` - Delete a menu category
- `POST /api/categories/:id/items` - Create a new menu item
- `PUT /api/items/:id` - Update a menu item
- `DELETE /api/items/:id` - Delete a menu item

#### Advanced Features API

- `GET /api/recommendations` - Get AI recommendations
- `POST /api/recommendations/generate` - Generate new AI recommendations
- `POST /api/recommendations/:id/apply` - Apply a recommendation
- `GET /api/analytics/summary` - Get analytics summary
- `GET /api/scheduled` - Get scheduled content
- `POST /api/scheduled` - Create scheduled content
- `DELETE /api/scheduled/:id` - Delete scheduled content
- `GET /api/collaborations` - Get collaborations
- `POST /api/collaborations` - Create a collaboration
- `PUT /api/collaborations/:id` - Update a collaboration
- `DELETE /api/collaborations/:id` - Delete a collaboration

## Deployment

### Local Deployment

For local development and testing:

```bash
python -m src.main
```

### Production Deployment

For production deployment, we recommend using Gunicorn with Nginx:

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create a systemd service file**
   ```
   [Unit]
   Description=Linkak Gunicorn Service
   After=network.target

   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/path/to/linkak
   Environment="PATH=/path/to/linkak/venv/bin"
   ExecStart=/path/to/linkak/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 src.main:app

   [Install]
   WantedBy=multi-user.target
   ```

3. **Configure Nginx**
   ```
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Enable and start the service**
   ```bash
   sudo systemctl enable linkak
   sudo systemctl start linkak
   ```

5. **Set up SSL with Let's Encrypt**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

### Docker Deployment

Linkak can also be deployed using Docker:

1. **Build the Docker image**
   ```bash
   docker build -t linkak .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 80:5000 --name linkak linkak
   ```

## GitHub Upload Instructions

Follow these steps to upload Linkak to your GitHub repository:

1. **Create a new repository on GitHub**
   - Go to GitHub and log in
   - Click the "+" icon in the top right and select "New repository"
   - Name your repository (e.g., "linkak")
   - Choose public or private visibility
   - Click "Create repository"

2. **Initialize Git in your local Linkak directory**
   ```bash
   cd /path/to/linkak
   git init
   ```

3. **Add your GitHub repository as remote**
   ```bash
   git remote add origin https://github.com/yourusername/linkak.git
   ```

4. **Create a .gitignore file**
   ```bash
   echo "venv/
   *.pyc
   __pycache__/
   instance/
   .env
   *.db
   .DS_Store" > .gitignore
   ```

5. **Add, commit, and push your files**
   ```bash
   git add .
   git commit -m "Initial commit of Linkak"
   git push -u origin master
   ```

6. **Verify the upload**
   - Go to your GitHub repository page
   - Ensure all files are uploaded correctly
   - Check that sensitive files are not included

## Troubleshooting

### Common Issues

#### Application won't start
- Check if all dependencies are installed
- Verify the database connection
- Ensure the port is not in use

#### Database errors
- Check database connection string
- Ensure database user has proper permissions
- Verify database schema is up to date

#### Authentication issues
- Clear browser cookies
- Reset password if necessary
- Check for correct username/email

#### Deployment issues
- Verify server permissions
- Check firewall settings
- Ensure proper configuration of web server

### Logging

Linkak logs important events to help with troubleshooting:

- Application logs: `logs/app.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`

## FAQ

### General Questions

**Q: What makes Linkak different from Linktree?**
A: Linkak offers advanced features like custom domain URL shortening, business menu builder, AI recommendations, advanced analytics, scheduled content, and team collaboration, all designed for professional use.

**Q: Is Linkak free to use?**
A: Linkak offers a free tier with basic features, as well as premium tiers for advanced features.

**Q: Can I use my own domain with Linkak?**
A: Yes, Linkak supports custom domains for both your profile and shortened URLs.

### Technical Questions

**Q: What technologies does Linkak use?**
A: Linkak is built with Flask (Python) for the backend, SQLAlchemy for database operations, and modern HTML/CSS/JavaScript for the frontend.

**Q: Can I extend Linkak with my own features?**
A: Yes, Linkak is designed to be extensible. You can add your own features by creating new routes and models.

**Q: Is Linkak mobile-friendly?**
A: Yes, Linkak is fully responsive and works well on mobile devices.

### Feature Questions

**Q: How does the URL shortener work?**
A: Linkak's URL shortener creates short, memorable links that redirect to your original URLs. It also provides analytics and QR code generation.

**Q: What can I do with the business menu builder?**
A: You can create digital menus for restaurants or businesses, with categories, items, prices, and images. These menus can be added to your profile or shared directly.

**Q: How do AI recommendations help me?**
A: AI recommendations analyze your profile and visitor behavior to suggest improvements to your layout, content, and theme for better engagement.

**Q: Can I schedule content changes?**
A: Yes, you can schedule links, themes, and profile changes to activate or deactivate at specific times.

**Q: How does team collaboration work?**
A: You can invite team members to collaborate on your profile, menus, or other resources, with different permission levels for each collaborator.
