# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 18:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blooming', '0003_auto_20170319_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classroom',
            old_name='description',
            new_name='serial',
        ),
    ]
