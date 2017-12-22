# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from notifications.signals import notify
from authentication.models import Client
from django.contrib.auth.models import User
# Create your models here.


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was saved')


post_save.connect(my_handler, sender=Client.user)


class Order_List(models.Model):
    order_id = models.IntegerField()
    username = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    order_date = models.DateField()
    delivery_date = models.DateField()
    action = models.CharField(max_length=100)
