# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0003_auto_20151014_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='promocode_title',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='Promocode Title'),
        ),
    ]
