# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150508_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='uuid',
            field=models.UUIDField(serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='privatemessage',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='userchannel',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='userserver',
            name='uuid',
            field=models.UUIDField(serialize=False, primary_key=True),
        ),
    ]
