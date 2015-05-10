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

from core.models import UserServer, UserChannel, Message, Conversation, \
    Channel, PrivateMessage


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


def create_message_for_user(user, channel_id, text):
    """
    Create a new message
    """
    uc = UserChannel.objects.get(
        channel_id=channel_id, user_server__user=user)
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


def get_conversation(conversation_id):
    """
    Get a channel by ID
    """
    try:
        return Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return None


def create_pm(sender, text, user_channel_id):
    """
    Create a new message
    """
    try:
        lc = UserChannel.objects.get(id=user_channel_id)
        uc = UserChannel.objects.get(channel_id=lc.channel_id, nickname=sender)
    except UserChannel.DoesNotExist:
        uc = UserChannel(channel_id=lc.channel_id, nickname=sender)
        uc.save()
    try:
        conv = Conversation.objects.get(
            Q(user_channel_1__in=[lc, uc]) &
            Q(user_channel_2__in=[lc, uc]))
    except Exception:
        conv = Conversation(user_channel_1=lc, user_channel_2=uc)
        conv.save()
    pm = PrivateMessage(conversation=conv, user_channel=uc, text=text)
    pm.save()
    return pm


def get_users_for_pm(pm):
    """
    docstring for get_users_for_pm
    """
    r = []
    try:
        r.append(pm.conversation.user_channel_1.user_server.user)
    except AttributeError:
        pass
    try:
        r.append(pm.conversation.user_channel_2.user_server.user)
    except AttributeError:
        pass
    return r


def create_pm_for_user(conversation_id, text, user):
    """
    docstring for create_pm_for_user
    """
    # conv = Conversation.objects.get()
    pass


def get_user_channel(user_channel_id):
    """
    docstring for get_user_channel
    """
    try:
        return UserChannel.objects.get(id=user_channel_id)
    except UserChannel.DoesNotExist:
        return None


def get_user_server(user_server_id):
    """
    docstring for get_user_channel
    """
    try:
        return UserServer.objects.get(id=user_server_id)
    except UserServer.DoesNotExist:
        return None
