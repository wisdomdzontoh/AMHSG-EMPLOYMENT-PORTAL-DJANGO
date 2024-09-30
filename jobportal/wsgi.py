"""
WSGI config for jobportal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')

application = get_wsgi_application()

app = application

from whitenoise import WhiteNoise

# Import BASE_DIR from settings
from .settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_tour.settings')

application = get_wsgi_application()

application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
