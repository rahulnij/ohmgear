# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='folder',
            table='ohmgear_folders_folder',
        ),
        migrations.AlterModelTable(
            name='foldertype',
            table='ohmgear_folders_foldertype',
        ),
    ]
