# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150507_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchannel',
            name='channel',
            field=models.ForeignKey(related_name='user_channels', default=1, to='core.Channel'),
            preserve_default=False,
        ),
    ]
