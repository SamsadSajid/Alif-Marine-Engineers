# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import hashlib
import os.path
import urllib
from django.conf import settings
# Create your models here.


class Order_List(models.Model):
    order_id = models.IntegerField()
    username = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    order_date = models.DateField()
    delivery_date = models.DateField()
    action = models.CharField(max_length=100)


class ProductList(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40)
    uploaded_by = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    product_image = models.FileField(upload_to='media/')
    choice = (('available', 'available'), ('unavailable', 'unavailable'))
    product_available = models.CharField(max_length=15, choices=choice)
    product_description = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'product_list'

    def __str__(self):
        return self.product_name
