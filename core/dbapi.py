#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: dbapi.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

from django.db.models import Q

from core.models import UserServer, UserChannel, Message, Conversation, Channel


def get_all_user_channels():
    """
    docstring for get_all_user_channels
    """
    return UserChannel.objects.all()


def create_message(sender, channel_id, text, user_channel_id):
    """
    Create a new message
    """
    try:
        uc = UserChannel.objects.get(channel_id=channel_id, nickname=sender)
    except UserChannel.DoesNotExist:
        uc = UserChannel(channel_id=channel_id, nickname=sender)
        uc.save()
    message = Message(channel_id=channel_id, user_channel=uc, text=text)
    message.save()
    return message


def get_users_for_channel_id(channel_id):
    """
    docstring for get_users_for_channel_id
    """
    ucs = UserChannel.objects.filter(channel_id=channel_id)
    return [uc.user_server.user for uc in ucs if uc.user_server]


def get_user_servers(user):
    """
    docstring for get_user_servers
    """
    return UserServer.objects.filter(user=user)


def get_user_channels(user_servers):
    """
    docstring for get_user_channels
    """
    return UserChannel.objects.filter(user_server__in=user_servers)


def get_conversations(user_channels):
    """
    docstring for get_conversations
    """
    return Conversation.objects.filter(
        Q(user_channel_1__in=user_channels) |
        Q(user_channel_2__in=user_channels))


def get_channel(channel_id):
    """
    Get a channel by ID
    """
    try:
        return Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return None
