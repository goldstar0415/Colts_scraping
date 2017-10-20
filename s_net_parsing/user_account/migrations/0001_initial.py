# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 18:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import user_account.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='users_avatar/', verbose_name='Users image')),
                ('bio', models.TextField(blank=True, max_length=400, null=True, verbose_name='Short biography')),
                ('country_name', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country of origin')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='Company name')),
                ('birth_date', models.DateField(null=True, verbose_name='Birth date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]