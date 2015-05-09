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

from django.http import JsonResponse
from tokenapi.decorators import token_required


@token_required
def init(request):
    return JsonResponse({
        'user': request.user.to_dict(with_sensitive_data=True),
    })
