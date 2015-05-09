# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_privatemessage_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('mode', models.CharField(default=b'', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='UserServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('label', models.CharField(default=b'My IRC Server', max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('nickname', models.CharField(max_length=256)),
                ('realname', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='server',
        ),
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='hostname',
            new_name='host',
        ),
        migrations.RemoveField(
            model_name='message',
            name='from_account',
        ),
        migrations.RemoveField(
            model_name='message',
            name='to_server',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='from_account',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='to_account',
        ),
        migrations.RemoveField(
            model_name='server',
            name='uuid',
        ),
        migrations.AddField(
            model_name='server',
            name='is_sasl',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='server',
            name='is_ssl',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='server',
            name='port',
            field=models.PositiveIntegerField(default=6667, blank=True),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.AddField(
            model_name='userserver',
            name='server',
            field=models.ForeignKey(related_name='user_servers', to='core.Server'),
        ),
        migrations.AddField(
            model_name='userserver',
            name='user',
            field=models.ForeignKey(related_name='user_servers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userchannel',
            name='user_server',
            field=models.ForeignKey(related_name='user_channels', to='core.UserServer'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='user_channel_1',
            field=models.ForeignKey(related_name='+', to='core.UserChannel'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='user_channel_2',
            field=models.ForeignKey(related_name='+', to='core.UserChannel'),
        ),
        migrations.AddField(
            model_name='channel',
            name='server',
            field=models.ForeignKey(related_name='channels', to='core.Server'),
        ),
        migrations.AddField(
            model_name='message',
            name='channel',
            field=models.ForeignKey(related_name='messages', default='', to='core.Channel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='user_channel',
            field=models.ForeignKey(related_name='messages', default=1, to='core.UserChannel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='conversation',
            field=models.ForeignKey(related_name='private_messages', default=1, to='core.Conversation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='user_channel',
            field=models.ForeignKey(related_name='private_messages', default=1, to='core.UserChannel'),
            preserve_default=False,
        ),
    ]
