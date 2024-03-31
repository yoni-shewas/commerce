"""
Gunicorn config for your Django project.

For more information on Gunicorn configuration, see
https://docs.gunicorn.org/en/stable/configure.html
"""

bind = '0.0.0.0:8000'  # Example bind address and port
workers = 3  # Example number of worker processes
