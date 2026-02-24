import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poison_detection.settings")

# WSGI application object used by Gunicorn in production on Render
app = get_wsgi_application()

