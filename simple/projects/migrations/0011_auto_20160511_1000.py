# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-11 10:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20160511_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='owner',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='projectactivity',
            old_name='owner',
            new_name='user',
        ),
    ]