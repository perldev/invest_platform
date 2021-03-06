# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-10 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investdeals',
            options={'ordering': ('-id',), 'verbose_name': 'Deal', 'verbose_name_plural': 'Deals'},
        ),
        migrations.AlterField(
            model_name='investdeals',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investdeals',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
