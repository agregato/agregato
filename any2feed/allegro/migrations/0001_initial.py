# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-11 10:16
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
            name='AllegroWatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('notify', models.BooleanField(default=False, verbose_name='notify')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'allegro watch',
                'verbose_name_plural': 'allegro watches',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allegro_id', models.CharField(max_length=255, verbose_name='allegro id')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('price', models.CharField(max_length=255, verbose_name='price')),
                ('href', models.CharField(max_length=255, verbose_name='href')),
                ('image_url', models.CharField(max_length=255, verbose_name='allegro image')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='add_date')),
                ('watch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allegro.AllegroWatch', verbose_name='watch')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ['-add_date'],
                'get_latest_by': 'add_date',
            },
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('watch', 'allegro_id')]),
        ),
    ]
