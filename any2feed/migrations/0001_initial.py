# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-11 10:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('regexp', models.CharField(blank=True, max_length=255, null=True, verbose_name='regexp')),
                ('xpath', models.CharField(blank=True, max_length=255, null=True, verbose_name='xpath')),
            ],
            options={
                'verbose_name': 'field definition',
                'verbose_name_plural': 'field definitions',
            },
        ),
        migrations.CreateModel(
            name='FieldInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='content')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='any2feed.FieldDefinition', verbose_name='field definition')),
            ],
            options={
                'verbose_name': 'field instance',
                'verbose_name_plural': 'field instances',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regexp', models.CharField(max_length=255, verbose_name='regexp')),
            ],
            options={
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='title')),
                ('href', models.CharField(blank=True, max_length=255, null=True, verbose_name='href')),
                ('content', models.TextField(blank=True, null=True, verbose_name='content')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='add_date')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ['-add_date'],
                'get_latest_by': 'add_date',
            },
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('title_regexp', models.CharField(blank=True, max_length=255, null=True, verbose_name='title regexp')),
                ('title_xpath', models.CharField(blank=True, max_length=255, null=True, verbose_name='title xpath')),
                ('content_regexp', models.CharField(blank=True, max_length=255, null=True, verbose_name='content regexp')),
                ('content_xpath', models.CharField(blank=True, max_length=255, null=True, verbose_name='content xpath')),
                ('href_regexp', models.CharField(blank=True, max_length=255, null=True, verbose_name='href regexp')),
                ('href_xpath', models.CharField(blank=True, max_length=255, null=True, verbose_name='href xpath')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('notify', models.CharField(blank=True, max_length=255, verbose_name='notify')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'watch',
                'verbose_name_plural': 'watches',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='watch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='any2feed.Watch', verbose_name='watch'),
        ),
        migrations.AddField(
            model_name='filter',
            name='watch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='any2feed.Watch', verbose_name='watch'),
        ),
        migrations.AddField(
            model_name='fieldinstance',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='any2feed.Item', verbose_name='item'),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='watch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='any2feed.Watch', verbose_name='watch'),
        ),
    ]