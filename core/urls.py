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

from core.views import init, channel, conversation, message, user_channel, \
    user_server

urlpatterns = [
    url(r'^init$', init),
    url(r'^channels/(?P<channel_id>.{36})$', channel),
    url(r'^conversations/(?P<conversation_id>.{36})$', conversation),
    url(r'^userChannels/(?P<user_channel_id>.{36})$', user_channel),
    url(r'^userServers/(?P<user_server_id>.{36})$', user_server),
    url(r'^message$', message),
]
