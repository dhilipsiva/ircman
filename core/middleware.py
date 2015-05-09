#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: middleware.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""
import traceback

from threading import local, current_thread

_thread_locals = local()


class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        print exception
        traceback.print_exc()


class GlobalUserMiddleware(object):
    """
    Sets the current authenticated user in threading locals

    Usage example:
        from core.middleware import get_current_user
        user = get_current_user()
    """
    def process_request(self, request):
        setattr(
            _thread_locals, 'user_{0}'.format(current_thread().name),
            request.user)

    def process_response(self, request, response):
        key = 'user_{0}'.format(current_thread().name)
        if not hasattr(_thread_locals, key):
            return response
        delattr(_thread_locals, key)
        return response


def get_current_user():
    return getattr(
        _thread_locals, 'user_{0}'.format(current_thread().name), None)
