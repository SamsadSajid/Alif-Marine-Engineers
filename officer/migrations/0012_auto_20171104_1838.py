# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officer', '0011_auto_20171104_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
