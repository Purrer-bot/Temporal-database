# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-07 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20181207_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='row1',
            field=models.CharField(max_length=50),
        ),
    ]
