#! /bin/bash
#
# model_diagram.sh
# Copyright (C) 2015 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
#

python manage.py graph_models core -o generated/models.png
