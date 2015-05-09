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
    message = dumps({
        'rooms': rooms,
        'event': event,
        'data': data,
    }, cls=DjangoJSONEncoder)
    return redis.publish(channel, message)


def notify(rooms, event, data):
    """
    docstring for notify
    """
    return _redis_call('notify', data, rooms, event)


def notify_message(rooms, message, notify_type=NotifyEnum.INFO):
    """
    Send a message to the user
    """
    data = {
        "message": message,
        "notifyType": notify_type
    }
    return notify(rooms, "message", data)


def notify_message_info(rooms, message):
    return notify_message(rooms, message, NotifyEnum.INFO)


def notify_message_success(rooms, message):
    return notify_message(rooms, message, NotifyEnum.SUCCESS)


def notify_message_warning(rooms, message):
    return notify_message(rooms, message, NotifyEnum.WARNING)


def notify_message_alert(rooms, message):
    return notify_message(rooms, message, NotifyEnum.ALERT)


def notify_message_error(rooms, message):
    return notify_message(rooms, message, NotifyEnum.ERROR)


def setup_client(data):
    """
    docstring for setup_client
    """
    return _redis_call('setupClient', data, [], None)
