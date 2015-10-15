# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.contacts.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('promocode_title', models.CharField(max_length=50, null=True, verbose_name='Promocode Title')),
                ('promocode_worth', models.CharField(max_length=500, null=True, verbose_name='Promocode Worth')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('expiry_date', models.DateTimeField(max_length=50, null=True, verbose_name='Expiry Date')),
                ('user_type', models.IntegerField(null=True, verbose_name=apps.contacts.models.Contact)),
                ('no_of_use', models.IntegerField(null=True, verbose_name=b'users.User')),
            ],
            options={
                'db_table': 'ohmgear_promocodes',
            },
        ),
    ]
