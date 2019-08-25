# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .common import *  # noqa

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w1kxu^l=@pnsf!5piqz6!!5kdcdpo79y6jebbp+2244yjm*#+k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
DATABASES['default']['NAME'] = 'recipe_site_dev'
DATABASES['default']['USER'] = 'recipe'
DATABASES['default']['PASSWORD'] = 'Recipe1234'
DATABASES['default']['TEST'] = {'CHARSET': 'utf8'}
DATABASES['default']['HOST'] = 'recipe_site_dev_db'
DATABASES['default']['PORT'] = '5432'

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += ['debug_toolbar']

INTERNAL_IPS = ['127.0.0.1',]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions']

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# corsheaders
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
