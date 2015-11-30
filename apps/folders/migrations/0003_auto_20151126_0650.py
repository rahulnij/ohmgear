# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0002_auto_20151102_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folder',
            old_name='businesscard',
            new_name='businesscard_id',
        ),
        migrations.AlterField(
            model_name='folder',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='created date', blank=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='foldername',
            field=models.CharField(max_length=30, verbose_name='folder name', error_messages={b'blank': b'Folder name can not be empty.'}),
        ),
        migrations.AlterField(
            model_name='folder',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='updated date', blank=True),
        ),
    ]
