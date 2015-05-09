#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: notify.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

from json import dumps
from redis import Redis

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from constants import NotifyEnum

redis = Redis(settings.REDIS_HOST, settings.REDIS_PORT)


def _redis_call(channel, data, rooms, event):
    """
    docstring for notify
    """
    toast = dumps({
        'rooms': rooms,
        'event': event,
        'data': data,
    }, cls=DjangoJSONEncoder)
    return redis.publish(channel, toast)


def notify(rooms, event, data):
    """
    docstring for notify
    """
    return _redis_call('notify', data, rooms, event)


def notify_message_new(rooms, data):
    """
    docstring for notify_message
    """
    return notify(rooms, 'message_new', data)


def notify_toast(rooms, toast, notify_type=NotifyEnum.INFO):
    """
    Send a toast to the user
    """
    data = {
        "toast": toast,
        "notifyType": notify_type
    }
    return notify(rooms, "toast", data)


def notify_toast_info(rooms, toast):
    return notify_toast(rooms, toast, NotifyEnum.INFO)


def notify_toast_success(rooms, toast):
    return notify_toast(rooms, toast, NotifyEnum.SUCCESS)


def notify_toast_warning(rooms, toast):
    return notify_toast(rooms, toast, NotifyEnum.WARNING)


def notify_toast_alert(rooms, toast):
    return notify_toast(rooms, toast, NotifyEnum.ALERT)


def notify_toast_error(rooms, toast):
    return notify_toast(rooms, toast, NotifyEnum.ERROR)


def setup_client(data):
    """
    docstring for setup_client
    """
    return _redis_call('setupClient', data, [], None)
