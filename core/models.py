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
    CharField, TextField, PositiveIntegerField


# App imports
from core.utils import random_uuid


def utc_now():
    """
    `now` with UTC
    """
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class User(AbstractUser):
    """
    A custom user so that we can add permissions easily
    """
    uuid = UUIDField(default=uuid4, editable=False)

    class Meta(AbstractUser.Meta):
        abstract = False

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = random_uuid()
        if 'pbkdf2_sha256' not in self.password:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def to_dict(self, with_sensitive_data=False):
        """
        Dictify user
        """
        d = {
            'id': self.uuid,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        if with_sensitive_data:
            d.update({
                'uuid': str(self.uuid),
                'email': self.email,
            })
        return d

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<User: %s>" % self.__str__()


class Server(Model):
    hostname = CharField(max_length=256)
    uuid = UUIDField(default=uuid4, editable=False)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': self.uuid,
            'host': self.host,
        }

    def __str__(self):
        return self.hostname

    def __repr__(self):
        return "<Server: %s>" % self.__str__()


class Account(Model):
    server = ForeignKey(Server)
    nickname = CharField(max_length=256)
    username = CharField(max_length=256)
    password = CharField(max_length=256)
    port = PositiveIntegerField(default=6667, blank=True)
    uuid = UUIDField(default=uuid4, editable=False)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': self.uuid,
            'nickname': self.nickname,
            'username': self.username,
            'port': self.port,
        }

    def __str__(self):
        return "%s - %s" % (self.server, self.username)

    def __repr__(self):
        return "<Account: %s>" % self.__str__()


class Message(Model):
    text = TextField()
    uuid = UUIDField(default=uuid4, editable=False)
    from_account = ForeignKey(Account)
    created_on = DateTimeField(auto_now_add=True)

    def to_dict(self):
        """
        Dictify user
        """
        return {
            'id': self.uuid,
            'text': self.text,
            'fromAccount': self.from_account_id,
        }

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Message: %s>" % self.__str__()


class PrivateMessage(Message):
    to_account = ForeignKey(Account)

    def to_dict(self):
        """
        Dictify user
        """
        d = super(PrivateMessage, self).to_dict()
        d.update({
            'text': self.text,
            'toAcount': self.to_acount_id,
        })

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<PrivateMessage: %s>" % self.__str__()