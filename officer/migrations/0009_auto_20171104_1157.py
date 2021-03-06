# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officer', '0008_auto_20171101_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=100)),
                ('rank', models.IntegerField()),
                ('review', models.CharField(max_length=250)),
                ('reviewed_by', models.CharField(max_length=100)),
                ('reviewed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'product_review',
            },
        ),
        migrations.AddField(
            model_name='productlist',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productlist',
            name='product_features',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='productlist',
            name='product_notes',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='productlist',
            name='product_porichiti',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productlist',
            name='product_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='productlist',
            name='product_image',
            field=models.FileField(upload_to='product_image/'),
        ),
        migrations.AlterField(
            model_name='productlist',
            name='product_name',
            field=models.CharField(max_length=100),
        ),
    ]
