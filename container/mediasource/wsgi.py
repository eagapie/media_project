"""
WSGI config for media project.
"""
import os
import sys

from os.path import dirname

PROJECT_ROOT    = os.path.abspath(os.path.dirname(__file__))

sys.path.append(dirname(PROJECT_ROOT))

DEBUG           = True
TEMPLATE_DEBUG  = DEBUG

ADMINS          = (
     ('Elena Agapie', 'eagapie@seas.harvard.edu'),
)

MANAGERS = ADMINS
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mediasource.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Apply WSGI middleware here.
#from helloworld.wsgi import HelloWorldApplication
#application = HelloWorldApplication(application)
