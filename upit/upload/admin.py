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
from django.db.models import Avg

##########################actions#######################################
def delete_marked(modeladmin, request, queryset):
    for obj in queryset:
        upload = UploadFile.objects.get(pk=obj.id)
        upload.delete()
delete_marked.short_description = "Delete selected Files"

#########################interfaces#####################################
class UploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'datetime', 'user', 'file', 'folder', 'type', 'extension', 'ratings']
    ordering = ['-datetime']
    search_fields = ['datetime', 'user', 'file', 'type', 'extension']
    list_filter = ['user', 'datetime', 'folder__name', 'type', 'extension']
    date_hierarchy = 'datetime'
    exclude = ['extension', 'type']
    actions = [delete_marked]
    
    def ratings(self, obj):
        ratings = FileRating.objects.filter(upload_file=obj).aggregate(Avg('stars'))
        return ratings["stars__avg"]
        

    def delete_model(self, request, obj):
        obj.delete()
        
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'public']
    search_fields = ['name']
    list_filter = ['public']
    actions = ['delete_selected']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['upload_file', 'stars', 'user']
    search_fields = ['upload_file']
    list_filter = ['upload_file', 'stars', 'user']
    actions = ['delete_selected']


admin.site.register(FileRating, RatingAdmin)
admin.site.register(UploadFile, UploadAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.disable_action('delete_selected')
