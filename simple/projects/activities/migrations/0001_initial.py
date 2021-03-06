# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-26 08:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0019_auto_20160526_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.CharField(blank=True, max_length=2000, null=True)),
                ('start_date', models.DateTimeField()),
                ('due_date', models.DateTimeField()),
                ('allowed_submissions', models.PositiveIntegerField(default=1)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'project activities',
            },
        ),
        migrations.CreateModel(
            name='ProjectActivityResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('body', models.CharField(max_length=20000)),
                ('number_submissions', models.PositiveIntegerField(default=0)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.ProjectActivity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='projectactivity',
            name='responses',
            field=models.ManyToManyField(related_name='responded_activity', through='activities.ProjectActivityResponse', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectactivity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='projectactivityresponse',
            unique_together=set([('user', 'activity')]),
        ),
    ]
