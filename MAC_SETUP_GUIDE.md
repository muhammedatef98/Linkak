# LinkHub Mac Setup and Domain Launch Guide

This comprehensive guide will walk you through setting up LinkHub on your Mac and launching it with your own domain.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running Locally](#running-locally)
4. [Domain Configuration](#domain-configuration)
5. [Production Deployment](#production-deployment)
6. [Maintenance](#maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed on your Mac:

- **Python 3.8+**: Check with `python3 --version` in Terminal
- **pip**: The Python package manager
- **Homebrew** (recommended): For installing additional dependencies
- **Git** (optional): For version control

If you need to install Python:
```bash
brew install python
```

If you need to install Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Installation

1. **Extract the LinkHub files**:
   Unzip the `LinkHub_without_venv.zip` file to your preferred location.

   ```bash
   unzip LinkHub_without_venv.zip -d ~/LinkHub
   cd ~/LinkHub
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install MySQL** (optional, for production):
   ```bash
   brew install mysql
   brew services start mysql
   ```

5. **Create a database** (optional, for production):
   ```bash
   mysql -u root -p
   ```
   
   In the MySQL prompt:
   ```sql
   CREATE DATABASE linkhub;
   CREATE USER 'linkhub_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON linkhub.* TO 'linkhub_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

## Running Locally

1. **Configure the database** (if using MySQL):
   
   Edit `src/main.py` and uncomment the database configuration section:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'linkhub_user')}:{os.getenv('DB_PASSWORD', 'your_password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'linkhub')}"
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   db.init_app(app)
   with app.app_context():
       db.create_all()
   ```

2. **Run the development server**:
   ```bash
   python -m src.main
   ```

3. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Domain Configuration

To use your own domain with LinkHub, you'll need:

1. **A registered domain name** (from providers like Namecheap, GoDaddy, etc.)
2. **A hosting service** or **VPS** (Virtual Private Server)

### Domain DNS Setup

1. **Log in to your domain registrar**
2. **Navigate to DNS settings**
3. **Add A records**:
   - Type: A
   - Host: @ (or leave blank for root domain)
   - Value: Your server's IP address
   - TTL: 3600 (or as recommended)

4. **Add CNAME record for www subdomain**:
   - Type: CNAME
   - Host: www
   - Value: your-domain.com (your root domain)
   - TTL: 3600

5. **Wait for DNS propagation** (can take up to 48 hours, but usually much faster)

## Production Deployment

For a production environment, you should use a WSGI server like Gunicorn:

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Create a production configuration file** `config.py`:
   ```python
   import os
   
   # Security settings
   SECRET_KEY = os.getenv('SECRET_KEY', 'generate-a-secure-random-key')
   DEBUG = False
   
   # Database settings
   DB_USERNAME = os.getenv('DB_USERNAME', 'linkhub_user')
   DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
   DB_HOST = os.getenv('DB_HOST', 'localhost')
   DB_PORT = os.getenv('DB_PORT', '3306')
   DB_NAME = os.getenv('DB_NAME', 'linkhub')
   ```

3. **Start with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 src.main:app
   ```

### Using Nginx as a Reverse Proxy

For better performance and security, use Nginx as a reverse proxy:

1. **Install Nginx**:
   ```bash
   brew install nginx
   ```

2. **Create an Nginx configuration file** `/usr/local/etc/nginx/servers/linkhub.conf`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /static {
           alias /path/to/LinkHub/src/static;
           expires 30d;
       }
   }
   ```

3. **Start Nginx**:
   ```bash
   brew services start nginx
   ```

### SSL Configuration with Let's Encrypt

For secure HTTPS:

1. **Install Certbot**:
   ```bash
   brew install certbot
   ```

2. **Obtain SSL certificate**:
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Follow the prompts** to complete the SSL setup

## Using a Process Manager

For keeping your application running:

1. **Install PM2**:
   ```bash
   npm install -g pm2
   ```

2. **Create a process file** `ecosystem.config.js`:
   ```javascript
   module.exports = {
     apps: [{
       name: "linkhub",
       script: "gunicorn",
       args: "-w 4 -b 0.0.0.0:8000 src.main:app",
       interpreter: "/path/to/LinkHub/venv/bin/python",
       env: {
         SECRET_KEY: "your-secure-key",
         DB_USERNAME: "linkhub_user",
         DB_PASSWORD: "your_password",
         DB_HOST: "localhost",
         DB_NAME: "linkhub"
       }
     }]
   }
   ```

3. **Start with PM2**:
   ```bash
   pm2 start ecosystem.config.js
   ```

4. **Set up PM2 to start on boot**:
   ```bash
   pm2 startup
   pm2 save
   ```

## Maintenance

### Database Backups

Regular database backups are essential:

```bash
# Create a backup
mysqldump -u linkhub_user -p linkhub > linkhub_backup_$(date +%Y%m%d).sql

# Restore from backup
mysql -u linkhub_user -p linkhub < linkhub_backup_20250529.sql
```

### Updating the Application

To update LinkHub:

1. **Stop the application**:
   ```bash
   pm2 stop linkhub
   ```

2. **Back up your data**:
   ```bash
   cp -r ~/LinkHub ~/LinkHub_backup_$(date +%Y%m%d)
   ```

3. **Update the code** (replace files or pull from git)

4. **Update dependencies**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Restart the application**:
   ```bash
   pm2 restart linkhub
   ```

## Troubleshooting

### Common Issues

1. **Application won't start**:
   - Check if port is already in use: `lsof -i :8000`
   - Verify virtual environment is activated
   - Check for syntax errors in your code

2. **Database connection issues**:
   - Verify MySQL is running: `brew services list`
   - Check credentials in configuration
   - Ensure database and user exist with proper permissions

3. **Static files not loading**:
   - Check Nginx configuration for static file path
   - Verify file permissions

4. **Domain not working**:
   - Verify DNS settings have propagated: `dig yourdomain.com`
   - Check Nginx configuration
   - Ensure firewall allows traffic on ports 80 and 443

### Getting Help

If you encounter issues not covered here:

1. Check the Flask and SQLAlchemy documentation
2. Search for specific error messages online
3. Check the LinkHub GitHub repository for known issues
4. Contact support at support@linkhub.com

## Conclusion

You now have LinkHub running on your Mac and accessible via your custom domain with HTTPS. The application is set up for production use with proper security measures and maintenance procedures.

For additional customization options, refer to the README.md file and the API documentation.
