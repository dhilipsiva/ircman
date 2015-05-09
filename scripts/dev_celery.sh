#! /bin/bash
#
# dev_celery.sh
# Copyright (C) 2015 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
#

celery -A ircman worker -l debug --concurrency=1
