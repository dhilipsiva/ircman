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

from node.notify import setup_client, notify_message_new, say, say_pm, \
    notify_pm_new

from core.dbapi import get_all_user_channels, create_message, \
    get_users_for_channel_id, create_message_for_user, create_pm, \
    get_users_for_pm, create_pm_for_user


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
    pm = create_pm(sender, text, user_channel_id)
    users = get_users_for_pm(pm)
    rooms = list(set([str(u.socket) for u in users]))
    return notify_pm_new(rooms, pm.to_dict())


@shared_task
def error(message, user_channel_id):
    print message, user_channel_id


@shared_task
def create_message_4_web(user, channel_id, text):
    """
    """
    message = create_message_for_user(user, channel_id, text)
    say(str(message.user_channel.id), text)
    users = get_users_for_channel_id(channel_id)
    rooms = list(set([str(u.socket) for u in users]))
    return notify_message_new(rooms, message.to_dict())


@shared_task
def create_pm_4_web(user, conversation_id, text):
    """
    """
    pm = create_pm_for_user(conversation_id, text, user)
    if pm.conversation.user_channel_1.user_server.user_id == user.id:
        sender = pm.conversation.user_channel_1
        to = pm.conversation.user_channel_2
    else:
        sender = pm.conversation.user_channel_2
        to = pm.conversation.user_channel_1
    say_pm(str(sender.id), to.nickname, text)
    users = get_users_for_pm(pm)
    print "==================================================="
    print users
    print "==================================================="
    rooms = [str(u.socket) for u in users]
    return notify_pm_new(rooms, pm.to_dict())
