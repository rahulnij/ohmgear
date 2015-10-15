# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='no_of_use',
            field=models.IntegerField(max_length=11, null=True, verbose_name='Maximum Usage'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='user_type',
            field=models.IntegerField(max_length=2, null=True, verbose_name='User Type'),
        ),
    ]
