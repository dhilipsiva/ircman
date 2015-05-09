#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: models.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

# Python imports
import datetime
from uuid import uuid4

# Django imports
from django.utils.timezone import utc
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ForeignKey, DateTimeField, UUIDField, \
    CharField, TextField, PositiveIntegerField, BooleanField


def utc_now():
    """
    `now` with UTC
    """
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class User(AbstractUser):
    """
    A custom user so that we can add permissions easily
    """
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    socket = UUIDField(default=uuid4, editable=False)

    class Meta(AbstractUser.Meta):
        abstract = False

    def save(self, *args, **kwargs):
        if 'pbkdf2_sha256' not in self.password:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def to_dict(self, with_sensitive_data=False):
        """
        Dictify user
        """
        d = {
            'id': str(self.id),
            'username': self.username,
            'firstName': self.first_name,
            'lastName': self.last_name,
        }
        if with_sensitive_data:
            d.update({
                'socket': str(self.socket),
                'email': self.email,
            })
        return d

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<User: %s>" % self.__str__()


class Server(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    host = CharField(max_length=256)
    port = PositiveIntegerField(default=6667, blank=True)
    is_ssl = BooleanField(default=False)
    is_sasl = BooleanField(default=False)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': str(self.id),
            'host': self.host,
            'port': self.port,
            'isSsl': self.is_ssl,
            'isSasl': self.is_sasl,
        }

    def __str__(self):
        return self.host

    def __repr__(self):
        return "<Server: %s>" % self.__str__()


class UserServer(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    user = ForeignKey(User, related_name="user_servers")
    server = ForeignKey(Server, related_name="user_servers")
    label = CharField(max_length=256, default="My IRC Server")
    username = CharField(max_length=256)
    password = CharField(max_length=256, null=True, blank=True)
    nickname = CharField(max_length=256)
    realname = CharField(max_length=256, null=True, blank=True)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': str(self.id),
            'userId': str(self.user_id),
            'server': self.server.to_dict(),
            'label': self.label,
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'realname': self.realname,
        }

    def __str__(self):
        return "%s - %s" % (self.user, self.server)

    def __repr__(self):
        return "<UserServer: %s>" % self.__str__()


class Channel(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    server = ForeignKey(Server, related_name="channels")
    name = CharField(max_length=256)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': str(self.id),
            'serverId': str(self.server_id),
            'name': self.name,
        }

    def __str__(self):
        return "%s - %s" % (self.server, self.name)

    def __repr__(self):
        return "<Channel: %s>" % self.__str__()


class UserChannel(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    user_server = ForeignKey(UserServer, related_name="user_channels")
    channel = ForeignKey(Channel, related_name="user_channels")
    nickname = CharField(max_length=256)
    password = CharField(max_length=256, null=True, blank=True)
    mode = CharField(max_length=16, null=True, blank=True)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            "id": str(self.id),
            "userServerId": str(self.user_server_id),
            "channelId": str(self.channel_id),
            "nickname": self.nickname,
            "password": self.password,
            "mode": self.mode,
        }

    def to_dict_deep(self):
        """
        Deep `to_dict`
        """
        d = self.to_dict()
        d['userServer'] = self.user_server.to_dict()
        d['channel'] = self.channel.to_dict()
        return d

    def __str__(self):
        return "%s - %s" % (self.channel, self.nickname)

    def __repr__(self):
        return "<UserChannel: %s>" % self.__str__()


class BaseMessage(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    text = TextField()
    created_on = DateTimeField(auto_now_add=True)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': str(self.id),
            'text': self.text,
            'createdOn': self.created_on,
        }

    class Meta:
        abstract = True


class Message(BaseMessage):
    channel = ForeignKey(Channel, related_name="messages")
    user_channel = ForeignKey(UserChannel, related_name="messages")

    def to_dict(self):
        """
        Dictify user
        """
        d = super(Message, self).to_dict()
        d.update({
            'fromAccount': self.from_account_id,
        })
        return d

    def __repr__(self):
        return "<Message: %s>" % self.__str__()


class Conversation(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    user_channel_1 = ForeignKey(UserChannel, related_name='+')
    user_channel_2 = ForeignKey(UserChannel, related_name='+')


class PrivateMessage(BaseMessage):
    conversation = ForeignKey(Conversation, related_name='private_messages')
    user_channel = ForeignKey(UserChannel, related_name='private_messages')
    read = BooleanField(default=False)

    def to_dict(self):
        """
        Dictify user
        """
        d = super(PrivateMessage, self).to_dict()
        d.update({
            'fromAccount': str(self.from_account_id),
            'toAcount': str(self.to_acount_id),
            'read': self.read,
        })

    def __repr__(self):
        return "<PrivateMessage: %s>" % self.__str__()
