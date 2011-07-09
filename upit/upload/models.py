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
        

class Folder(models.Model):
    name = models.CharField("Name", max_length=200, unique=True)
    public = models.BooleanField("Public")
    
    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"

    def __unicode__(self):
        return self.name
