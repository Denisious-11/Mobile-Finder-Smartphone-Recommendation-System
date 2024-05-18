# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-06-20 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=20)),
                ('email_id', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]