# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-07 10:22
from __future__ import unicode_literals

import core.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', core.fields.RestrictedFile(blank=True, null=True, upload_to=b'projects/attachment')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_attachments', to='comments.Comment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
