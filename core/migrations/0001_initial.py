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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('socket_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
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
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('port', models.PositiveIntegerField(default=6667, blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.ForeignKey(related_name='messages_sent', to='core.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.ForeignKey(related_name='private_messages_sent', to='core.Account')),
                ('to_account', models.ForeignKey(related_name='private_messages_received', to='core.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=256)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='to_server',
            field=models.ForeignKey(related_name='messages_received', to='core.Server'),
        ),
        migrations.AddField(
            model_name='account',
            name='server',
            field=models.ForeignKey(related_name='accounts', to='core.Server'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
