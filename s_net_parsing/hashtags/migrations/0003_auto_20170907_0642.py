# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 06:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hashtags', '0002_auto_20170905_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hashtag', to=settings.AUTH_USER_MODEL),
        ),
    ]
