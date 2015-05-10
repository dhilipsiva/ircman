#! /bin/bash
#
# runcelery.sh
# Copyright (C) 2015 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
#


set -e
# go in your project root
cd %(code_root)s
# set PYTHONPATH to cwd
export PYTHONPATH=`pwd`
# activate the virtualenv
source %(virtenv)s/bin/activate
# start celery with all options earlier declared in fabfile.py

exec celery -A ircman worker -l info
