# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-20 08:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('startpage', '0002_auto_20161010_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransfers',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442'),
        ),
        migrations.AddField(
            model_name='banktransfers',
            name='processed_pub_date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0432\u043e\u0434\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='clientprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
