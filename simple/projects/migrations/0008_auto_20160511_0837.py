# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-11 08:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcomment',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectcomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='ProjectComment',
        ),
    ]
