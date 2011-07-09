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
from upit.upload.models import *
from django.contrib import admin

class UploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'datetime', 'user', 'file', 'folder']
    ordering = ['-datetime']
    search_fields = ['datetime', 'user', 'file']
    list_filter = ['user', 'datetime', 'user__username', 'folder__name']
    date_hierarchy = 'datetime'

class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'public']
    search_fields = ['name']
    list_filter = ['public']

admin.site.register(UploadFile, UploadAdmin)
admin.site.register(Folder, FolderAdmin)
