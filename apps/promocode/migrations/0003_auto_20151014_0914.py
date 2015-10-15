# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0002_auto_20151014_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='no_of_use',
            field=models.IntegerField(null=True, verbose_name='Maximum Usage'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='user_type',
            field=models.IntegerField(null=True, verbose_name='User Type'),
        ),
    ]
