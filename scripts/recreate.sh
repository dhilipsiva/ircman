#! /bin/bash
#
# recreate.sh
# Copyright (C) 2015 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
#


psql -f scripts/recreate.sql -d postgres
