"""
Gunicorn Configuration for Linkak Production
Optimized for performance, security, and monitoring
"""

import os
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = int(os.environ.get('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = os.environ.get('WORKER_CLASS', 'gevent')
worker_connections = int(os.environ.get('WORKER_CONNECTIONS', 1000))
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Restart workers after this much time has passed
timeout = 30
graceful_timeout = 30
keepalive = 2

# Maximum number of simultaneous clients
worker_connections = 1000

# The socket to bind to
bind = "0.0.0.0:8000"

# SSL Configuration (if using HTTPS directly)
# keyfile = "/app/ssl/key.pem"
# certfile = "/app/ssl/cert.pem"

# Logging
accesslog = "/app/logs/gunicorn_access.log"
errorlog = "/app/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Process naming
proc_name = "linkak"

# User and group to run as
# user = "linkak"
# group = "linkak"

# Preload application for better performance
preload_app = True

# Enable automatic worker restarts
max_requests = 1000
max_requests_jitter = 50

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Monitoring
statsd_host = None  # Set to your StatsD server if available
statsd_prefix = "linkak"

# Worker temporary directory
worker_tmp_dir = "/dev/shm"

# Debugging (set to False in production)
reload = False
spew = False

# Hooks for application lifecycle
def on_starting(server):
    server.log.info("Starting Linkak server...")

def on_reload(server):
    server.log.info("Reloading Linkak server...")

def when_ready(server):
    server.log.info("Linkak server is ready. Listening on: %s", server.address)

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    pass

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    pass

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def pre_request(worker, req):
    # Log the start time of each request
    worker.log.debug("%s %s" % (req.method, req.uri))

def post_request(worker, req, environ, resp):
    # You can add custom logging here
    pass

def on_exit(server):
    server.log.info("Shutting down Linkak server...")

# Environment variables
raw_env = [
    'FLASK_ENV=production',
]