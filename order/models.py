from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from officer.models import ProductList


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=250)
    zip = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery = models.DateField(null=True)
    choices = (('In Progress', 'In Progress'), ('Done', 'Done'), ('Rejected', 'Rejected'))
    status = models.CharField(max_length=15, default="In Progress", choices=choices)
    updatedByManager = models.CharField(max_length=100)
    updatedByManagerId = models.IntegerField(null=True)
    updatedByManagerAt = models.DateTimeField(auto_now_add=True)
    # paid option will be available in the pro version
    # paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(ProductList, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
