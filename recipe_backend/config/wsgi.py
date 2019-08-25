"""
WSGI config for recipe_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from django.core.wsgi import get_wsgi_application


os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"

application = get_wsgi_application()
