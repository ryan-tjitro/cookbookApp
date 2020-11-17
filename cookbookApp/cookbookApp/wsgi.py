#!/usr/bin/env python

"""
WSGI config for cookbookApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/mnt/c/Users/rctji/Projects/cookbookApp/cookbookApp')
sys.path.append('/mnt/c/Users/rctji/Projects/cookbookApp/cookbookApp/cookbookApp')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cookbookApp.settings')

application = get_wsgi_application()
