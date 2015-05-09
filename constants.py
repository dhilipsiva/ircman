#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: constants.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

import inspect


def user_attributes(cls):
    defaults = dir(type('defaults', (object,), {}))  # gives all inbuilt attrs
    return [
        item[0] for item in inspect.getmembers(cls) if item[0] not in defaults]


def choices(cls):
    """
    Decorator to set `CHOICES` attribute
    """
    _choices = []
    for attr in user_attributes(cls):
        val = getattr(cls, attr)
        _choices.append((val, attr))
    setattr(cls, 'CHOICES', tuple(_choices))
    return cls


@choices
class NotifyEnum:
    UNKNOWN = -1
    INFO = 0
    SUCCESS = 2
    WARNING = 3
    ALERT = 4
    ERROR = 5
