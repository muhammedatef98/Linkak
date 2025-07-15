# Production-ready Dockerfile for Linkak
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=src/main.py \
    FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r linkak && useradd -r -g linkak linkak

# Copy requirements first for better caching
COPY requirements.txt requirements-production.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/backups /app/static/uploads \
    && chown -R linkak:linkak /app

# Copy configuration files
COPY deploy/nginx.conf /etc/nginx/sites-available/linkak
COPY deploy/supervisor.conf /etc/supervisor/conf.d/linkak.conf

# Enable nginx site
RUN ln -s /etc/nginx/sites-available/linkak /etc/nginx/sites-enabled/ \
    && rm /etc/nginx/sites-enabled/default

# Set proper permissions
RUN chmod +x deploy/entrypoint.sh \
    && chown -R linkak:linkak /app

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/api/health || exit 1

# Switch to non-root user
USER linkak

# Entry point
ENTRYPOINT ["./deploy/entrypoint.sh"]