#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: urls.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

from django.conf.urls import url

from core.views import init, channel

urlpatterns = [
    url(r'^init$', init),
    url(r'^channels/(?P<channel_id>.{36})$', channel),
]
