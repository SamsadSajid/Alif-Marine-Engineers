# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 15:58
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20171014_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='+123456789', max_length=128),
        ),
    ]