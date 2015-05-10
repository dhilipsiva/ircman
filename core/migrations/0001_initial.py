# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('socket', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('channel', models.ForeignKey(related_name='messages', to='core.Channel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('conversation', models.ForeignKey(related_name='private_messages', to='core.Conversation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('host', models.CharField(max_length=256)),
                ('port', models.PositiveIntegerField(default=6667, blank=True)),
                ('is_ssl', models.BooleanField(default=False)),
                ('is_sasl', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserChannel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('nickname', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256, null=True, blank=True)),
                ('mode', models.CharField(max_length=16, null=True, blank=True)),
                ('channel', models.ForeignKey(related_name='user_channels', to='core.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='UserServer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('label', models.CharField(default=b'My IRC Server', max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256, null=True, blank=True)),
                ('nickname', models.CharField(max_length=256)),
                ('realname', models.CharField(max_length=256, null=True, blank=True)),
                ('server', models.ForeignKey(related_name='user_servers', to='core.Server')),
                ('user', models.ForeignKey(related_name='user_servers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userchannel',
            name='user_server',
            field=models.ForeignKey(related_name='user_channels', to='core.UserServer', null=True),
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='user_channel',
            field=models.ForeignKey(related_name='private_messages', to='core.UserChannel'),
        ),
        migrations.AddField(
            model_name='message',
            name='user_channel',
            field=models.ForeignKey(related_name='messages', to='core.UserChannel'),
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
    ]
