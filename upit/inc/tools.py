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


def gen_filelist(files):    
    # get mimetypes and pictures
    new_files = []
    mime_path = os_join(settings.STATIC_URL, "images/mimetypes/")
    for f in files:
        if f.file.path.lower().endswith(".h"):
            new_files.append( ( os_join(mime_path, "h.png"), f, basename(f.file.path), "src") )
        
        # picture
        elif f.file.path.lower().endswith(".png") or f.file.path.lower().endswith(".jpg") or f.file.path.lower().endswith(".jpeg") or f.file.path.lower().endswith(".gif"):
            new_files.append( ( "%s%s" % (settings.MEDIA_URL, f.file), f, basename(f.file.path), "pic") )       
        
        elif f.file.path.lower().endswith("makefile"):
            new_files.append( ( os_join(mime_path, "make.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".pdf"):
            new_files.append( ( os_join(mime_path, "pdf.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".xsl") or f.file.path.lower().endswith(".ods") or f.file.path.lower().endswith(".xslx"):
            new_files.append( ( os_join(mime_path, "excel.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".odt") or f.file.path.lower().endswith(".doc") or f.file.path.lower().endswith(".docx"):
            new_files.append( ( os_join(mime_path, "word.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".hpp"):
            new_files.append( ( os_join(mime_path, "hpp.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".sh"):
            new_files.append( ( os_join(mime_path, "bash.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".html") or f.file.path.lower().endswith(".htm"):
            new_files.append( ( os_join(mime_path, "html.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".c"):
            new_files.append( ( os_join(mime_path, "c.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".cpp"):
            new_files.append( ( os_join(mime_path, "cpp.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".csharp"):
            new_files.append( ( os_join(mime_path, "csharp.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".deb"):
            new_files.append( ( os_join(mime_path, "deb.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".exe"):
            new_files.append( ( os_join(mime_path, "exe.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".flv"):
            new_files.append( ( os_join(mime_path, "flv.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".jar"):
            new_files.append( ( os_join(mime_path, "jar.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".java"):
            new_files.append( ( os_join(mime_path, "java.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".js"):
            new_files.append( ( os_join(mime_path, "js.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".mp3") or f.file.path.lower().endswith(".ogg") or f.file.path.lower().endswith(".aac") or f.file.path.lower().endswith(".flac"):
            new_files.append( ( os_join(mime_path, "music.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".pl"):
            new_files.append( ( os_join(mime_path, "perl.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".php"):
            new_files.append( ( os_join(mime_path, "php.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".xcf"):
            new_files.append( ( os_join(mime_path, "ink.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".py"):
            new_files.append( ( os_join(mime_path, "py.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".rpm"):
            new_files.append( ( os_join(mime_path, "rpm.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".rb"):
            new_files.append( ( os_join(mime_path, "ruby.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".svg"):
            new_files.append( ( os_join(mime_path, "svg.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".tex"):
            new_files.append( ( os_join(mime_path, "tex.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".tgz") or f.file.path.lower().endswith(".gz"):
            new_files.append( ( os_join(mime_path, "tgz.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".torrent"):
            new_files.append( ( os_join(mime_path, "torrent.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".xml"):
            new_files.append( ( os_join(mime_path, "xml.png"), f, basename(f.file.path), "src") )
        
        elif f.file.path.lower().endswith(".zip") or f.file.path.lower().endswith(".7z") or f.file.path.lower().endswith(".rar") or f.file.path.lower().endswith(".bz2") or f.file.path.lower().endswith(".lzma"):
            new_files.append( ( os_join(mime_path, "zip.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".ogv") or f.file.path.lower().endswith(".mkv") or f.file.path.lower().endswith(".avi") or f.file.path.lower().endswith(".mp4") or f.file.path.lower().endswith(".wmv"):
            new_files.append( ( os_join(mime_path, "video.png"), f, basename(f.file.path), "bin") )
        
        elif f.file.path.lower().endswith(".awk"):
            new_files.append( ( os_join(mime_path, "awk.png"), f, basename(f.file.path), "src") )
        
        else:
            new_files.append( ( os_join(mime_path, "bin.png"), f, basename(f.file.path), "bin") )
    
    return new_files
