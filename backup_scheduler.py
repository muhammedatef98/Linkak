#!/usr/bin/env python3
"""
Linkak Backup Scheduler
Manages automated backups with flexible scheduling and retention policies
"""

import os
import sys
import time
import logging
import subprocess
import schedule
from datetime import datetime, timedelta
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/backup_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BackupScheduler:
    """Automated backup scheduler for Linkak"""
    
    def __init__(self):
        self.backup_script = '/app/scripts/backup.sh'
        self.backup_dir = '/app/backups'
        self.retention_days = int(os.environ.get('BACKUP_RETENTION_DAYS', 30))
        self.max_backups = int(os.environ.get('MAX_BACKUPS', 50))
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Make backup script executable
        if os.path.exists(self.backup_script):
            os.chmod(self.backup_script, 0o755)
        
        logger.info(f"Backup scheduler initialized with {self.retention_days} days retention")
    
    def run_backup(self, backup_type: str = 'scheduled'):
        """Execute backup script"""
        try:
            logger.info(f"Starting {backup_type} backup...")
            
            # Run backup script
            result = subprocess.run(
                [self.backup_script],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode == 0:
                logger.info(f"{backup_type.capitalize()} backup completed successfully")
                self.cleanup_old_backups()
                self.send_backup_notification(True, backup_type)
            else:
                logger.error(f"{backup_type.capitalize()} backup failed: {result.stderr}")
                self.send_backup_notification(False, backup_type, result.stderr)
                
        except subprocess.TimeoutExpired:
            logger.error(f"{backup_type.capitalize()} backup timed out")
            self.send_backup_notification(False, backup_type, "Backup timed out")
        except Exception as e:
            logger.error(f"{backup_type.capitalize()} backup error: {e}")
            self.send_backup_notification(False, backup_type, str(e))
    
    def cleanup_old_backups(self):
        """Remove old backup files based on retention policy"""
        try:
            logger.info("Cleaning up old backups...")
            
            # Get current time
            now = datetime.now()
            cutoff_time = now - timedelta(days=self.retention_days)
            
            # Count and remove old files
            removed_count = 0
            backup_files = []
            
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    backup_files.append((filepath, file_time))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove files older than retention period
            for filepath, file_time in backup_files:
                if file_time < cutoff_time:
                    os.remove(filepath)
                    removed_count += 1
                    logger.info(f"Removed old backup: {os.path.basename(filepath)}")
            
            # Also enforce max backup limit
            if len(backup_files) > self.max_backups:
                files_to_remove = backup_files[self.max_backups:]
                for filepath, _ in files_to_remove:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        removed_count += 1
                        logger.info(f"Removed backup (max limit): {os.path.basename(filepath)}")
            
            logger.info(f"Cleanup completed. Removed {removed_count} old backup files")
            
        except Exception as e:
            logger.error(f"Backup cleanup error: {e}")
    
    def send_backup_notification(self, success: bool, backup_type: str, error_msg: str = None):
        """Send backup status notification"""
        try:
            status = "SUCCESS" if success else "FAILED"
            message = f"Linkak {backup_type} backup {status}"
            
            if not success and error_msg:
                message += f": {error_msg}"
            
            # Send webhook notification
            webhook_url = os.environ.get('BACKUP_NOTIFICATION_URL')
            if webhook_url:
                import requests
                payload = {
                    'text': message,
                    'backup_type': backup_type,
                    'success': success,
                    'timestamp': datetime.now().isoformat()
                }
                
                if error_msg:
                    payload['error'] = error_msg
                
                requests.post(webhook_url, json=payload, timeout=10)
            
            # Send email notification for failures
            if not success:
                email_to = os.environ.get('BACKUP_ALERT_EMAIL')
                if email_to:
                    self.send_email_alert(email_to, message, error_msg)
                    
        except Exception as e:
            logger.error(f"Failed to send backup notification: {e}")
    
    def send_email_alert(self, email_to: str, message: str, error_msg: str = None):
        """Send email alert for backup failures"""
        try:
            # This would integrate with your email system
            # For now, just log the intention
            logger.info(f"Would send email alert to {email_to}: {message}")
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    def get_backup_status(self) -> Dict[str, Any]:
        """Get current backup status and statistics"""
        try:
            backup_files = []
            total_size = 0
            
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    backup_files.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                    total_size += stat.st_size
            
            # Sort by creation time (newest first)
            backup_files.sort(key=lambda x: x['created'], reverse=True)
            
            return {
                'total_backups': len(backup_files),
                'total_size_bytes': total_size,
                'total_size_human': self.format_bytes(total_size),
                'retention_days': self.retention_days,
                'max_backups': self.max_backups,
                'backup_files': backup_files[:10],  # Show last 10 backups
                'last_backup': backup_files[0]['created'] if backup_files else None
            }
            
        except Exception as e:
            logger.error(f"Error getting backup status: {e}")
            return {'error': str(e)}
    
    def format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def setup_schedule(self):
        """Setup backup schedule based on configuration"""
        # Parse schedule from environment variable
        backup_schedule = os.environ.get('BACKUP_SCHEDULE', '0 2 * * *')  # Default: Daily at 2 AM
        
        # For simplicity, we'll support a few common patterns
        if backup_schedule == '0 2 * * *':  # Daily at 2 AM
            schedule.every().day.at("02:00").do(self.run_backup, 'daily')
            logger.info("Scheduled daily backup at 2:00 AM")
            
        elif backup_schedule.startswith('0 2 * * 0'):  # Weekly on Sunday
            schedule.every().sunday.at("02:00").do(self.run_backup, 'weekly')
            logger.info("Scheduled weekly backup on Sunday at 2:00 AM")
            
        elif backup_schedule.startswith('0 */6'):  # Every 6 hours
            schedule.every(6).hours.do(self.run_backup, 'hourly')
            logger.info("Scheduled backup every 6 hours")
            
        else:
            # Default to daily if can't parse
            schedule.every().day.at("02:00").do(self.run_backup, 'daily')
            logger.warning(f"Could not parse schedule '{backup_schedule}', using daily default")
        
        # Also schedule cleanup independently
        schedule.every().day.at("03:00").do(self.cleanup_old_backups)
        logger.info("Scheduled daily cleanup at 3:00 AM")
    
    def run_immediate_backup(self):
        """Run immediate backup (for manual trigger)"""
        logger.info("Running immediate backup...")
        self.run_backup('immediate')
    
    def run_scheduler(self):
        """Run the backup scheduler"""
        logger.info("Starting backup scheduler...")
        self.setup_schedule()
        
        # Run initial backup if no backups exist
        if not os.listdir(self.backup_dir):
            logger.info("No existing backups found, running initial backup...")
            self.run_backup('initial')
        
        # Main scheduler loop
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                logger.info("Backup scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)


def main():
    """Main entry point"""
    scheduler = BackupScheduler()
    
    # Check if this is a one-time backup request
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        scheduler.run_immediate_backup()
    elif len(sys.argv) > 1 and sys.argv[1] == 'status':
        status = scheduler.get_backup_status()
        print(f"Backup Status: {status}")
    else:
        # Run continuous scheduler
        scheduler.run_scheduler()


if __name__ == '__main__':
    main()