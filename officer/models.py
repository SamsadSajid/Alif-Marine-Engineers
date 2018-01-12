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
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40)
    uploaded_by = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    product_image = models.FileField(upload_to='media/')
    choice = (('available', 'available'), ('unavailable', 'unavailable'))
    product_available = models.CharField(max_length=15, choices=choice)
    product_porichiti = models.CharField(max_length=100, null=True, blank=True) # I am really out of variable names
    product_description = models.CharField(max_length=300, null=True, blank=True)
    product_notes = models.CharField(max_length=300, null=True, blank=True)
    product_features = models.CharField(max_length=300, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'product_list'
        ordering = "-uploaded_at",

    def __str__(self):
        return self.product_name

    # Method for indexing the model
    def indexing(self):
        from elastic_search.search import ProductIndex
        obj = ProductIndex(
            meta={'id': self.id},
            product_id=self.product_id,
            product_name=self.product_name,
            slug=self.slug,
            uploaded_by=self.uploaded_by,
            uploaded_at=self.uploaded_at,
            product_available=self.product_available,
            product_porichiti=self.product_porichiti,
            product_description=self.product_description,
            product_notes=self.product_notes,
            product_features=self.product_features,
            quantity=self.quantity,
            price=self.price
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class ProductReview(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)
    review = models.CharField(max_length=250, null=True)
    reviewed_by = models.CharField(max_length=100)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_review'
