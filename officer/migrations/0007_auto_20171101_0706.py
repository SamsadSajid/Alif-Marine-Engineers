# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officer', '0006_auto_20171101_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlist',
            name='slug',
            field=models.SlugField(max_length=40),
        ),
    ]