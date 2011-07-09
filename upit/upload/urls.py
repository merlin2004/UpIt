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

from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    url(r'^$', 'upit.upload.views.index', name='index'),
    url(r'^show/src/(?P<srcid>\d+)/$', 'upit.upload.views.src_view', name='src_view'),
    url(r'^show/pic/(?P<srcid>\d+)/$', 'upit.upload.views.pic_view', name='pic_view'),
    url(r'^pic/(?P<srcid>\d+)/$', 'upit.upload.views.pic', name='pic'),
    url(r'^thumb/(?P<srcid>\d+)/$', 'upit.upload.views.thumb', name='thumb'),
    url(r'^download/(?P<srcid>\d+)/$', 'upit.upload.views.download', name='download'),

    # login and logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'upit/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '../'}, name='logout'),
)
