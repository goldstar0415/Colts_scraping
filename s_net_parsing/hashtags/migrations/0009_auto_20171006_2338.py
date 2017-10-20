# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtag_network', '0001_initial'),
        ('social_parsing', '0005_auto_20170927_2008'),
        ('hashtags', '0008_auto_20171004_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='last_scraped',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='network',
        ),
        migrations.AddField(
            model_name='hashtag',
            name='networks',
            field=models.ManyToManyField(blank=True, related_name='hashtags', through='hashtag_network.HashTagNetwork', to='social_parsing.Network', verbose_name='Social network'),
        ),
    ]
