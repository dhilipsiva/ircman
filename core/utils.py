#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: utils.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

import hmac
import hashlib
from uuid import uuid1, uuid5

from django.conf import settings


def random_uuid():
    """
    Get a random UUID
    """
    return str(uuid5(uuid1(), str(uuid1())))


def hmac_sign(data):
    """
    Sign recovery token
    """
    return hmac.new(
        settings.HMAC_SECRET, str(data), hashlib.sha1).hexdigest()


def hmac_verify(data, signature):
    """
    Verify the data and signature
    """
    evaluated_sign = hmac_sign(str(data))
    return evaluated_sign == signature
