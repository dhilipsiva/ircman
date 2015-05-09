#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

from __future__ import absolute_import

"""
File name: tasks.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

from celery import shared_task

from node.notify import setup_client, notify_message_new

from core.dbapi import get_all_user_channels, create_message, \
    get_users_for_channel_id


@shared_task
def init():
    for uc in get_all_user_channels():
        if uc.user_server:
            setup_client(uc.to_dict_deep())


@shared_task
def message(sender, channel_id, text, user_channel_id):
    message = create_message(sender, channel_id, text, user_channel_id)
    users = get_users_for_channel_id(channel_id)
    rooms = list(set([str(u.socket) for u in users]))
    return notify_message_new(rooms, message.to_dict())


@shared_task
def pm(sender, text, user_channel_id):
    print sender, text, user_channel_id


@shared_task
def error(message, user_channel_id):
    print message, user_channel_id
