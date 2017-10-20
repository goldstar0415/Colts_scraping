# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 12:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_parsing', '0002_auto_20170907_1129'),
        ('accounts', '0002_account_network_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Social network account', 'verbose_name_plural': 'Social network accounts'},
        ),
        migrations.RemoveField(
            model_name='account',
            name='network_id',
        ),
        migrations.AddField(
            model_name='account',
            name='network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social_parsing.Network', verbose_name='Social network'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(verbose_name='Active/Blocked'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_limited',
            field=models.BooleanField(verbose_name='Queries limit'),
        ),
        migrations.AlterField(
            model_name='account',
            name='login',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Network login'),
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Network password'),
        ),
        migrations.AlterField(
            model_name='account',
            name='token',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Network token'),
        ),
    ]