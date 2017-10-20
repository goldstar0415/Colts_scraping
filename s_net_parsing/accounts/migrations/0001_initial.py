# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=400, null=True, verbose_name='Токен соцсети')),
                ('login', models.CharField(blank=True, max_length=100, null=True, verbose_name='Логин соцсети')),
                ('password', models.CharField(blank=True, max_length=100, null=True, verbose_name='Пароль соцсети')),
                ('is_limited', models.BooleanField(verbose_name='Лимит запросов')),
                ('is_active', models.BooleanField(verbose_name='Активен/Заблокирован')),
            ],
            options={
                'verbose_name': 'Аккаунт соцсети',
                'verbose_name_plural': 'Аккаунты соцсетей',
            },
        ),
    ]