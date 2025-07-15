#!/bin/bash

# Linkak Production Entrypoint Script
# This script prepares and starts all services for production

set -e

echo "Starting Linkak Production Setup..."

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    until PGPASSWORD=$DB_PASSWORD psql -h "db" -U "linkak_user" -d "linkak_db" -c '\q'; do
        echo "Database is unavailable - sleeping"
        sleep 1
    done
    echo "Database is ready!"
}

# Function to wait for Redis
wait_for_redis() {
    echo "Waiting for Redis to be ready..."
    until redis-cli -h redis -p 6379 ping; do
        echo "Redis is unavailable - sleeping"
        sleep 1
    done
    echo "Redis is ready!"
}

# Create necessary directories
mkdir -p /app/logs /app/backups /app/static/uploads

# Set proper permissions
chown -R linkak:linkak /app/logs /app/backups /app/static/uploads

# Wait for external services if in Docker environment
if [ "$FLASK_ENV" = "production" ] && [ -n "$DATABASE_URL" ]; then
    wait_for_db
fi

if [ -n "$REDIS_URL" ]; then
    wait_for_redis
fi

# Database initialization and migration
echo "Initializing database..."
cd /app
python << PYTHON_EOF
from src.main import app, db
from src.config import get_config

app.config.from_object(get_config())

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database initialized successfully!")
PYTHON_EOF

# Generate SSL certificate if not exists (self-signed for development)
if [ ! -f "/app/ssl/cert.pem" ] && [ ! -f "/app/ssl/key.pem" ]; then
    echo "Generating self-signed SSL certificate..."
    mkdir -p /app/ssl
    openssl req -x509 -newkey rsa:4096 -keyout /app/ssl/key.pem -out /app/ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Linkak/OU=IT/CN=linkak.local"
    chmod 600 /app/ssl/key.pem
    chmod 644 /app/ssl/cert.pem
fi

# Setup nginx configuration
echo "Setting up Nginx..."
# Copy nginx configuration if it doesn't exist
if [ ! -f "/etc/nginx/sites-available/linkak" ]; then
    cp /app/deploy/nginx.conf /etc/nginx/sites-available/linkak
    ln -sf /etc/nginx/sites-available/linkak /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
fi

# Test nginx configuration
nginx -t

# Create htpasswd file for admin protection if it doesn't exist
if [ ! -f "/app/.htpasswd" ] && [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
    echo "Creating admin authentication file..."
    htpasswd -cb /app/.htpasswd "$ADMIN_USERNAME" "$ADMIN_PASSWORD"
fi

# Setup log rotation
echo "Setting up log rotation..."
cat > /etc/logrotate.d/linkak << LOGROTATE_EOF
/app/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 linkak linkak
    postrotate
        supervisorctl restart linkak
    endscript
}
LOGROTATE_EOF

echo "Starting Supervisor..."
exec supervisord -c /app/deploy/supervisor.conf
