# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templates',
            name='id',
        ),
        migrations.AlterField(
            model_name='templates',
            name='slug',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
