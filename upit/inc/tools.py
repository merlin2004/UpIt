#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
UpIt

Copyright (C) 2011 Bernhard Posselt, bernhard.posselt@gmx.at

UpIt is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

UpIt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar. If not, see <http://www.gnu.org/licenses/>.

"""

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import smart_str

from os.path import basename
from os.path import join as os_join
import os
import mimetypes

def render(request, tpl, tplvars={}):
    """Shortcut for renewing csrf cookie and passing request context
    
    Keyword arguments:
    tpl -- the template we want to use
    args -- the template variables

    """
    tplvars.update(csrf(request))
    tplvars["LOGIN_REDIRECT"] = reverse("upit:login")
    return render_to_response(tpl, tplvars,
                               context_instance=RequestContext(request))


def serve_file(path):
    # serve files which require authentification with apache 
    # mod_xsendfile
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(basename(path))
    response['X-Sendfile'] = smart_str(path)
    return response
    
    
def serve_img(path):
    # serve images which require authentification with apache 
    # mod_xsendfile
    response = HttpResponse(mimetype=mimetypes.guess_type(path)) 
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(basename(path))
    response['X-Sendfile'] = smart_str(path)
    return response

