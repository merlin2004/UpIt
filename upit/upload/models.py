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

# define extensions and types
img_types = ["png", "gif", "jpg", "jpeg"]
src_types = ["c", "cpp", "h", "hpp", "cs", "js", "php", "rb", "py", "sh", 
             "html", "htm", "java", "pl", "tex", "xsl", "xml", "awk", ]
# only add those vid types that we want to support playing directly"
vid_types = ["webm", "ogv"]
aud_types = ["ogg", "oga"]


# Files
class UploadFile(models.Model):
    user = models.ForeignKey("auth.User")
    datetime = models.DateTimeField("Date of upload", auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
    folder = models.ForeignKey("Folder")
    FILE_TYPE_CHOICES=(
        (u"img", u"Image"),
        (u"src", u"Source/Text"),
        (u"bin", u"Binary"),
        (u"aud", u"Audio"),
        (u"vid", u"Video"),
    )
    type = models.CharField("Filetype", choices=FILE_TYPE_CHOICES, max_length=3)
    extension = models.CharField("Extension", max_length=4)


    def get_thumb(self):
        """Returns the thumbnail path according to the filetype
        """
        mime_url_path = os.path.join(settings.STATIC_URL, "images/mimetypes/")
        mime_path = os.path.join(settings.STATIC_ROOT, "images/mimetypes/")
        # ignore images, they're passed in the tpl directly
        if self.type == "img":
            return ""
        elif self.type == "aud":
            return "%saud.png" % (mime_url_path)
        elif self.type == "vid":
            return "%svid.png" % (mime_url_path)
        else:
            # look if there are extensions
            icon = "%s.png" % self.extension
            if icon in os.listdir(mime_path):
                return "%s%s.png" % (mime_url_path, self.extension)
            # otherwise return the bin img
            else:
                return "%sbin.png" % (mime_url_path)


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
        scale = 128
        # first save the picture
        self.extension = os.path.splitext(self.file.path)[1][1:].lower()
        if self.extension in img_types:
            self.type = u"img"
        elif self.extension in vid_types:
            self.type = u"vid"
        elif self.extension in aud_types:
            self.type = u"aud"
        elif self.extension in src_types:
            self.type = u"src"
        else:
            self.type = u"bin"
        super(UploadFile, self).save()

        # now produce thumb
        img = self.file
        img_path = img.path
        if self.type == "img":
            if self.extension == "jpg":
                img_type = "jpeg"
            else:
                img_type = self.extension
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
        if self.type == "img":
            if self.extension == "jpg":
                img_type = "jpeg"
            else:
                img_type = self.extension
            # check if there is a thumbnail
            thumb_path = "%suploads/thumbs/%i.%s" % (settings.MEDIA_ROOT, self.id, img_type)
            try:
                os.unlink(thumb_path)
            # case file could not be deleted keep silent
            except OSError:
                print "could not delete %s" % thumb_path
        # finally delete the file itself
        try:
            self.file.delete(save=False)
            super(UploadFile, self).delete()
        except OSError:
            print "could not delete %s" % self.file.path


class Folder(models.Model):
    name = models.CharField("Name", max_length=200, unique=True)
    public = models.BooleanField("Public")
    
    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"

    def __unicode__(self):
        return self.name
