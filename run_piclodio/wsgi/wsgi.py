import os
import sys

path = '/var/www/Piclodio2'
if path not in sys.path:
    sys.path.append(path)
    
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'piclodio.settings'
application = get_wsgi_application()

