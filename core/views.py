#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: views.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

from django.http import JsonResponse
from tokenapi.decorators import token_required

from core.dbapi import get_user_servers, get_user_channels, get_conversations


@token_required
def init(request):
    user_servers = get_user_servers(request.user)
    user_channels = get_user_channels(user_servers)
    conversations = get_conversations(user_channels)
    return JsonResponse({
        'user': request.user.to_dict(with_sensitive_data=True),
        'user_servers': [us.to_dict() for us in user_servers],
        'user_channels': [uc.to_dict() for uc in user_channels],
        'conversations': [c.to_dict() for c in conversations],
    })
