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
Date created: 2015-05-10
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

try:
    index_html = open(settings.INDEX_HTML, 'r').read()
except Exception, e:
    index_html = "<h1>Error: index.html not found</h1>"


@csrf_exempt
def index(request):
    """
    docstring for index
    """
    return HttpResponse(index_html)
