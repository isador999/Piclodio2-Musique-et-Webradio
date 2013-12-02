import os
import sys

path = '/media/nico/Dropbox/Code_Source/Piclodio/src/Piclodio2'
if path not in sys.path:
    sys.path.append(path)
    
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'piclodio.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

