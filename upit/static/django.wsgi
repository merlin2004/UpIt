#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
from os.path import dirname
# append upit's parent directory to the sys path
relPath = dirname(dirname(dirname( os.path.abspath(__file__) )))
sys.path.append(os.path.abspath(relPath))

os.environ['DJANGO_SETTINGS_MODULE'] = 'upit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
