# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_auto_20171112_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.CharField(choices=[('Senior', 'Senior Officer'), ('Junior', 'Junior Officer')], max_length=20),
        ),
    ]