#! /bin/bash
#
# rungunicorn.sh
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
# start gunicorn with all options earlier declared in fabfile.py

gunicorn \
    -w %(gunicorn_workers)s \
    --user=%(deploy_user)s \
    --bind=%(gunicorn_bind)s \
    --log-level=%(gunicorn_loglevel)s \
    %(project)s.wsgi:application \
    --log-file=%(gunicorn_logfile)s 2>> %(gunicorn_logfile)s
