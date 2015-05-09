# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150508_1123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='socket_id',
            new_name='socket',
        ),
        migrations.AlterField(
            model_name='userchannel',
            name='user_server',
            field=models.ForeignKey(related_name='user_channels', to='core.UserServer', null=True),
        ),
    ]
