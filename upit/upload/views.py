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

from PIL import Image

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from upit.upload.models import *
from upit.upload.forms import *
from upit.inc.tools import render, gen_filelist, serve_file, serve_img



def index(request):
    """Default folder and itemsoverview
    """
    folder = request.GET.get("folder", False)
    if folder:
        files = UploadFile.objects.filter(folder__name=folder)
    else:
        if request.user.is_authenticated():
            files = UploadFile.objects.all()
        else:
            files = UploadFile.objects.filter(folder__public=True)
    
    # check if user is allowed to see folder
    try:
        selected_folder = Folder.objects.get(name=folder)
        if selected_folder.public == False and not request.user.is_authenticated():
            return HttpResponseRedirect( reverse('upit:login') )   
    except Folder.DoesNotExist:
        pass
        
    # get folders
    if request.user.is_authenticated():
        folders = Folder.objects.all()
    else:
        folders = Folder.objects.filter(public=True)
    
    new_files = gen_filelist(files)
    
    # get form
    if request.method == 'POST' and request.user.is_authenticated():
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return HttpResponseRedirect( reverse('upit:index') )
    else:
        form = UploadForm()
    return render(request, 'upit/index.html', 
                    {   
                        'form': form, 
                        'files': new_files, 
                        'folders': folders, 
                        'active': folder
                    }
                ) 


def src_view(request, srcid):
    """Show source of program language files
    """
    # get source
    src = UploadFile.objects.get(id=srcid)
    if src.folder.public or request.user.is_authenticated():
        return render(request, 'upit/src.html', {'file': src } ) 
    else:
        return HttpResponseRedirect( reverse('upit:login') )    


def pic_view(request, srcid):
    """Shows a site for pictures
    """
    # get pictures
    src = UploadFile.objects.get(id=srcid)
    if src.folder.public or request.user.is_authenticated():
        return render(request, 'upit/pic.html', {'pic': src } ) 
    else:
        return HttpResponseRedirect( reverse('upit:login') )


def download(request, srcid):
    """ download a file according to its id. checks for authorization
    """
    src = UploadFile.objects.get(id=srcid)
    if src.folder.public or request.user.is_authenticated():
        return serve_file(src.file.path)
    else:
        return HttpResponseRedirect( reverse('upit:login') )


def thumb(request, srcid):
    """create a thumb on the fly
    """
    scale = int(request.GET.get("scale", 128))
    
    src = UploadFile.objects.get(id=srcid)
    img = src.file
    if img.path.lower().endswith(".png"):
        img_type = "png"
    elif img.path.lower().endswith(".jpg") or img.path.lower().endswith(".jpeg"):
        img_type = "jpeg"
    
    ret_img = Image.open(img)
    ret_img.thumbnail((scale, scale), Image.ANTIALIAS)    
    response = HttpResponse(mimetype="image/%s" % img_type)
    ret_img.save(response, img_type.upper())
    
    if src.folder.public or request.user.is_authenticated():
        return response
    else:
        return HttpResponseRedirect( reverse('upit:login') )
        
        
def pic(request, srcid):
    """returns an image to the browser
    """

    src = UploadFile.objects.get(id=srcid)
    
    if src.folder.public or request.user.is_authenticated():
        return serve_img(src.file.path)
    else:
        return HttpResponseRedirect( reverse('upit:login') )
