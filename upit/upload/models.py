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

import os
from PIL import Image

from django.db import models
from django.conf import settings

# Files
class UploadFile(models.Model):
    user = models.ForeignKey("auth.User")
    datetime = models.DateTimeField("Date of upload", auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
    folder = models.ForeignKey("Folder")
        
    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ['-datetime']

    def save(self):
        """
        This is a custom save method for generating img thumbnails on 
        fileupload
        """
        # scale in pixels
        scale = 128 #px 
        # first save the picture
        super(UploadFile, self).save()
        # now create the thumbnail and save the thumb
        # to the uploads/thumbs directory if its an image
        img = self.file
        img_path = img.path
        extension = img_path.rsplit(".")[1].lower()
        # check for allowed extensions
        if extension in ["jpg", "jpeg", "png"]:
            # now get right mimetype        
            if extension == "png": 
                img_type = "png"
            else: 
                img_type = "jpeg"
            thumb = Image.open(img)
            thumb.thumbnail((scale, scale), Image.ANTIALIAS)
            # save thumb into thumb folder
            thumb_path = "%suploads/thumbs/%i.%s" % (settings.MEDIA_ROOT, self.id, img_type)
            thumb.save(thumb_path, img_type.upper())

    def delete(self):
        """
        This custom delete method is needed for deleting the thumbs
        """
        # first delete the thumb
        img = self.file
        img_path = img.path
        extension = img_path.rsplit(".")[1].lower()
        # check for allowed extensions
        if extension in ["jpg", "jpeg", "png"]:
            # now get right mimetype        
            if extension == "png": 
                img_type = "png"
            else: 
                img_type = "jpeg"
            # check if there is a thumbnail
            thumb_path = "%suploads/thumbs/%i.%s" % (settings.MEDIA_ROOT, self.id, img_type)
            try:
                os.unlink(thumb_path)
            # case file could not be deleted keep silent
            except OSError:
                pass
        # finally delete the file itself
        super(UploadFile, self).delete()


class Folder(models.Model):
    name = models.CharField("Name", max_length=200, unique=True)
    public = models.BooleanField("Public")
    
    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"

    def __unicode__(self):
        return self.name
