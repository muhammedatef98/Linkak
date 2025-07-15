#!/bin/bash

# Linkak Automated Backup Script
# Performs database and file backups with retention management

set -e

# Configuration
BACKUP_DIR="/app/backups"
DB_NAME="linkak_db"
DB_USER="linkak_user"
DB_HOST="${DB_HOST:-db}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting backup process at $(date)"

# Database backup
echo "Backing up database..."
PGPASSWORD="$DB_PASSWORD" pg_dump \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --no-password \
    --format=custom \
    --compress=9 \
    --file="$BACKUP_DIR/db_backup_$TIMESTAMP.dump"

# Verify database backup
if [ -f "$BACKUP_DIR/db_backup_$TIMESTAMP.dump" ]; then
    echo "Database backup completed: db_backup_$TIMESTAMP.dump"
else
    echo "ERROR: Database backup failed!"
    exit 1
fi

# Files backup (uploads, logs, etc.)
echo "Backing up application files..."
tar -czf "$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz" \
    -C /app \
    static/uploads \
    logs \
    --exclude='logs/*.log.gz' \
    2>/dev/null || echo "Some files may have been skipped"

echo "Files backup completed: files_backup_$TIMESTAMP.tar.gz"

# Configuration backup
echo "Backing up configuration..."
cp /app/.env "$BACKUP_DIR/env_backup_$TIMESTAMP" 2>/dev/null || echo "No .env file found"

# Clean up old backups
echo "Cleaning up old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "*.dump" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "env_backup_*" -mtime +$RETENTION_DAYS -delete

# Create backup summary
cat > "$BACKUP_DIR/backup_summary_$TIMESTAMP.txt" << SUMMARY_EOF
Backup Summary
Date: $(date)
Database backup: db_backup_$TIMESTAMP.dump
Files backup: files_backup_$TIMESTAMP.tar.gz
Configuration backup: env_backup_$TIMESTAMP

Database size: $(du -h "$BACKUP_DIR/db_backup_$TIMESTAMP.dump" | cut -f1)
Files size: $(du -h "$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz" | cut -f1)

Total backups in directory: $(ls -1 "$BACKUP_DIR"/*.dump 2>/dev/null | wc -l)
SUMMARY_EOF

# Upload to cloud storage (if configured)
if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$BACKUP_S3_BUCKET" ]; then
    echo "Uploading to S3..."
    aws s3 cp "$BACKUP_DIR/db_backup_$TIMESTAMP.dump" "s3://$BACKUP_S3_BUCKET/linkak/db/"
    aws s3 cp "$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz" "s3://$BACKUP_S3_BUCKET/linkak/files/"
    echo "Cloud backup completed"
fi

echo "Backup process completed successfully at $(date)"

# Send notification (if configured)
if [ -n "$BACKUP_NOTIFICATION_URL" ]; then
    curl -X POST "$BACKUP_NOTIFICATION_URL" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"Linkak backup completed successfully at $(date)\"}" \
        2>/dev/null || echo "Notification sending failed"
fi
