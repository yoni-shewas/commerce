"""
WSGI config for your Django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')

application = get_wsgi_application()

# Add the path to your Django project to sys.path
sys.path.append('C:\\Users\\PC\\Desktop\\S-L\\Python\\commerce')
