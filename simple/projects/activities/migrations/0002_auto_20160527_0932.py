# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-27 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectactivity',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
