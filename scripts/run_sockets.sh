#! /bin/bash
#
# run_sockets.sh
# Copyright (C) 2015 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
#

set -e
# go in your project root
cd %(sockets_path)s
# set PYTHONPATH to cwd
export PYTHONPATH=`pwd`
# activate the virtualenv
source %(nodeenv)s/bin/activate
# start gunicorn with all options earlier declared in fabfile.py

exec coffee index.coffee --host=172.31.58.191 --port=6379 >> %(sockets_logfile)s
