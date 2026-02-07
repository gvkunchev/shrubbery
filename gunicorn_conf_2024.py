"""Gunicorn *development* config file"""

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "shrubbery.wsgi:application"
# The granularity of Error log outputs
loglevel = "info"
# The number of worker processes for handling requests
workers = 1
threads = 4
preload_app=True
# The socket to bind
bind = "0.0.0.0:8024"
# Write access and error info to /var/log
accesslog = errorlog = "/var/log/gunicorn/dev_2024.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/dev_2024.pid"