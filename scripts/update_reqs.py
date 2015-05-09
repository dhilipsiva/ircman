#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: update_reqs.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-09
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""

import subprocess

dev_reqs = [req.lower() for req in [
    'pygraphviz',
    'django-extensions'
]]

test_reqs = [req.lower() for req in [
]]

ignore_reqs = [req.lower() for req in [
]]

dev_file = open('dev-requirements.txt', 'w')
test_file = open('test-requirements.txt', 'w')
production_file = open('requirements.txt', 'w')

output = subprocess.check_output("pip freeze", shell=True)

for req in output.split("\n"):
    if not req:
        continue
    package = req.split("==")[0].lower()
    if package in dev_reqs:
        dev_file.write(req + '\n')
    elif package in test_reqs:
        test_file.write(req + '\n')
    elif package not in ignore_reqs:
        production_file.write(req + '\n')
    else:
        print "%s ignored!" % req

dev_file.close()
test_file.close()
production_file.close()

print "requirements successfully updated!"
