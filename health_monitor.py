#!/usr/bin/env python3
"""
Linkak Health Monitor
Continuously monitors the health of the application and its dependencies
"""

import os
import sys
import time
import json
import logging
import requests
import psutil
from datetime import datetime
from typing import Dict, Any

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app, db
from config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/health_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class HealthMonitor:
    """Health monitoring service for Linkak"""
    
    def __init__(self):
        self.app = app
        self.app.config.from_object(get_config())
        self.check_interval = int(os.environ.get('HEALTH_CHECK_INTERVAL', 60))
        self.alert_threshold = int(os.environ.get('HEALTH_ALERT_THRESHOLD', 3))
        self.failure_counts = {}
        
    def check_application_health(self) -> Dict[str, Any]:
        """Check if the main application is responding"""
        try:
            response = requests.get(
                'http://localhost/api/health',
                timeout=10
            )
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'response_time': response.elapsed.total_seconds(),
                    'details': response.json()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}',
                    'response_time': response.elapsed.total_seconds()
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'response_time': None
            }
    
    def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            with self.app.app_context():
                start_time = time.time()
                result = db.engine.execute('SELECT 1')
                response_time = time.time() - start_time
                
                # Check connection pool status
                pool = db.engine.pool
                pool_status = {
                    'size': pool.size(),
                    'checked_in': pool.checkedin(),
                    'checked_out': pool.checkedout(),
                }
                
                return {
                    'status': 'healthy',
                    'response_time': response_time,
                    'pool_status': pool_status
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'response_time': None
            }
    
    def check_redis_health(self) -> Dict[str, Any]:
        """Check Redis connectivity and performance"""
        try:
            import redis
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
            r = redis.from_url(redis_url)
            
            start_time = time.time()
            r.ping()
            response_time = time.time() - start_time
            
            # Get Redis info
            info = r.info()
            memory_usage = info.get('used_memory_human', 'unknown')
            connected_clients = info.get('connected_clients', 0)
            
            return {
                'status': 'healthy',
                'response_time': response_time,
                'memory_usage': memory_usage,
                'connected_clients': connected_clients
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'response_time': None
            }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Load average
            load_avg = os.getloadavg()
            
            # Check if resources are critical
            critical_alerts = []
            if cpu_percent > 90:
                critical_alerts.append(f"High CPU usage: {cpu_percent}%")
            if memory_percent > 90:
                critical_alerts.append(f"High memory usage: {memory_percent}%")
            if disk_percent > 90:
                critical_alerts.append(f"High disk usage: {disk_percent}%")
            
            return {
                'status': 'critical' if critical_alerts else 'healthy',
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'load_average': load_avg,
                'alerts': critical_alerts
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_ssl_certificate(self) -> Dict[str, Any]:
        """Check SSL certificate validity"""
        try:
            import ssl
            import socket
            from datetime import datetime, timezone
            
            domain = os.environ.get('DOMAIN_NAME', 'localhost')
            if domain == 'localhost':
                return {'status': 'skipped', 'reason': 'localhost domain'}
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse expiry date
                    expiry_str = cert['notAfter']
                    expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                    expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                    
                    days_until_expiry = (expiry_date - datetime.now(timezone.utc)).days
                    
                    status = 'healthy'
                    if days_until_expiry < 7:
                        status = 'critical'
                    elif days_until_expiry < 30:
                        status = 'warning'
                    
                    return {
                        'status': status,
                        'days_until_expiry': days_until_expiry,
                        'expiry_date': expiry_str,
                        'issuer': cert['issuer']
                    }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        logger.info("Starting health check...")
        
        checks = {
            'application': self.check_application_health(),
            'database': self.check_database_health(),
            'redis': self.check_redis_health(),
            'system': self.check_system_resources(),
            'ssl': self.check_ssl_certificate(),
        }
        
        # Determine overall health
        overall_status = 'healthy'
        critical_issues = []
        warnings = []
        
        for check_name, result in checks.items():
            if result['status'] == 'unhealthy':
                overall_status = 'unhealthy'
                critical_issues.append(f"{check_name}: {result.get('error', 'Unknown error')}")
            elif result['status'] == 'critical':
                overall_status = 'critical'
                critical_issues.extend(result.get('alerts', [f"{check_name}: Critical issue"]))
            elif result['status'] == 'warning':
                warnings.append(f"{check_name}: {result.get('message', 'Warning')}")
        
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall_status,
            'checks': checks,
            'critical_issues': critical_issues,
            'warnings': warnings
        }
        
        # Log the results
        if overall_status == 'healthy':
            logger.info("Health check completed: All systems healthy")
        elif overall_status == 'critical':
            logger.error(f"Health check completed: Critical issues found: {critical_issues}")
        else:
            logger.warning(f"Health check completed: Issues found: {critical_issues}")
        
        return health_report
    
    def handle_failure(self, service_name: str, error: str):
        """Handle service failure with escalation"""
        self.failure_counts[service_name] = self.failure_counts.get(service_name, 0) + 1
        
        if self.failure_counts[service_name] >= self.alert_threshold:
            self.send_alert(service_name, error)
            # Reset counter after alerting
            self.failure_counts[service_name] = 0
    
    def send_alert(self, service_name: str, error: str):
        """Send alert notification"""
        alert_message = f"ALERT: {service_name} has failed {self.alert_threshold} times. Error: {error}"
        logger.error(alert_message)
        
        # Send webhook notification if configured
        webhook_url = os.environ.get('ALERT_WEBHOOK_URL')
        if webhook_url:
            try:
                payload = {
                    'text': alert_message,
                    'service': service_name,
                    'error': error,
                    'timestamp': datetime.now().isoformat()
                }
                requests.post(webhook_url, json=payload, timeout=10)
            except Exception as e:
                logger.error(f"Failed to send webhook alert: {e}")
        
        # Send email notification if configured
        email_to = os.environ.get('ALERT_EMAIL')
        if email_to:
            try:
                from flask_mail import Mail, Message
                mail = Mail(self.app)
                with self.app.app_context():
                    msg = Message(
                        subject=f"Linkak Alert: {service_name} Failure",
                        recipients=[email_to],
                        body=alert_message
                    )
                    mail.send(msg)
            except Exception as e:
                logger.error(f"Failed to send email alert: {e}")
    
    def save_health_report(self, report: Dict[str, Any]):
        """Save health report to file"""
        report_file = f"/app/logs/health_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # Load existing reports for the day
            reports = []
            if os.path.exists(report_file):
                with open(report_file, 'r') as f:
                    reports = json.load(f)
            
            # Add new report
            reports.append(report)
            
            # Keep only last 100 reports per day
            if len(reports) > 100:
                reports = reports[-100:]
            
            # Save updated reports
            with open(report_file, 'w') as f:
                json.dump(reports, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save health report: {e}")
    
    def run(self):
        """Run the health monitor continuously"""
        logger.info(f"Starting health monitor with {self.check_interval}s interval")
        
        while True:
            try:
                report = self.perform_health_check()
                self.save_health_report(report)
                
                # Handle failures
                for check_name, result in report['checks'].items():
                    if result['status'] in ['unhealthy', 'critical']:
                        self.handle_failure(check_name, result.get('error', 'Unknown error'))
                    else:
                        # Reset failure count on success
                        self.failure_counts[check_name] = 0
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Health monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                time.sleep(self.check_interval)


if __name__ == '__main__':
    monitor = HealthMonitor()
    monitor.run()