# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150508_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='socket_uuid',
            new_name='socket_id',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='message',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='server',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='userchannel',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='userserver',
            name='uuid',
        ),
        migrations.AddField(
            model_name='channel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='message',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='server',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='userchannel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='userserver',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
    ]
