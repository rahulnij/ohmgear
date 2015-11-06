# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('businesscards', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foldername', models.CharField(max_length=30, verbose_name='folder name')),
                ('foldertype', models.CharField(default=b'PR', max_length=2, verbose_name='folder type', choices=[(b'PR', b'Private')])),
                ('status', models.IntegerField(default=1, verbose_name='status')),
                ('created_date', models.DateTimeField(verbose_name='created date')),
                ('updated_date', models.DateTimeField(verbose_name='updated date')),
                ('businesscard', models.ForeignKey(db_column=b'businesscard_id', verbose_name='business card', to='businesscards.BusinessCard')),
                ('user_id', models.ForeignKey(db_column=b'user_id', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FolderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]
