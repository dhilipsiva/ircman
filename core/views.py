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

from celery import current_app
from django.http import JsonResponse, Http404
from tokenapi.decorators import token_required

from core.dbapi import get_user_servers, get_user_channels, get_channel, \
    get_conversations, get_conversation, get_user_channel, get_user_server


@token_required
def init(request):
    user_servers = get_user_servers(request.user)
    user_channels = get_user_channels(user_servers)
    conversations = get_conversations(user_channels)
    return JsonResponse({
        'user': request.user.to_dict(with_sensitive_data=True),
        'user_servers': [us.to_dict() for us in user_servers],
        'servers': [us.server.to_dict() for us in user_servers],
        'user_channels': [uc.to_dict() for uc in user_channels],
        'channels': [uc.channel.to_dict() for uc in user_channels],
        'conversations': [c.to_dict() for c in conversations],
        'messages': [
            m.to_dict()
            for uc in user_channels
            for m in uc.channel.messages.all()
        ],
        'private_messages': [
            pm.to_dict()
            for conv in conversations
            for pm in conv.private_messages.all()
        ],
    })


@token_required
def channel(request, channel_id):
    """
    Get channel data
    """
    channel = get_channel(channel_id=channel_id)
    if not channel:
        return Http404
    return JsonResponse({
        'channel': channel.to_dict(),
    })


@token_required
def conversation(request, conversation_id):
    """
    Get channel data
    """
    conversation = get_conversation(conversation_id=conversation_id)
    if not conversation:
        raise Http404
    return JsonResponse({
        'conversation': conversation.to_dict(),
    })


@token_required
def user_channel(request, user_channel_id):
    """
    Get channel data
    """
    user_channel = get_user_channel(user_channel_id)
    if not user_channel:
        raise Http404
    return JsonResponse({
        'userChannel': user_channel.to_dict(),
    })


@token_required
def user_server(request, user_server_id):
    """
    Get channel data
    """
    user_server = get_user_server(user_server_id)
    if not user_channel:
        raise Http404
    return JsonResponse({
        'userServer': user_server.to_dict(),
    })


@token_required
def message(request):
    """
    Create a new message
    """
    text = request.POST.get("text")
    modelType = request.POST.get("modelType")
    uuid = request.POST.get("modelId")
    if modelType == 'channel':
        current_app.send_task(
            "core.tasks.create_message_4_web",
            args=[request.user, uuid, text])
    else:
        current_app.send_task(
            "core.tasks.create_pm_4_web",
            args=[request.user, uuid, text])
    return JsonResponse({})
