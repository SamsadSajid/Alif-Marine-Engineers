"""
This python file will create a flag that will allow
to check in the html file, if there is any review for the product. If
there is, the reviews will be showed. Otherwise,
it will show to write a review.
"""

from django import template
from django.template import Library
from officer.models import ProductList
from decimal import getcontext, Decimal

register = Library()


@register.assignment_tag()
def check_review_status(product_review):
    value = [p for p in product_review if p.review]
    if value:
        return True
    else:
        return False


@register.assignment_tag()
def get_name(item):
    product = ProductList.objects.get(id=item.product_id)
    name = product.product_name
    return name


@register.assignment_tag()
def get_description(item):
    product = ProductList.objects.get(id=item.product_id)
    description = product.product_description
    return description


@register.assignment_tag()
def get_price(item):
    return item.price * item.quantity


@register.assignment_tag()
def get_total_price(order_item):
    total = 0
    for item in order_item:
        total += get_price(item)
    return total


@register.assignment_tag()
def get_tax_percentage():
    return Decimal(5.00)


@register.assignment_tag()
def get_tax(order_item):
    total = get_total_price(order_item)
    return total * get_tax_percentage()/Decimal(100.00)


@register.assignment_tag()
def get_shipping():
    return Decimal(15.00)


@register.assignment_tag()
def get_total(order_item):
    return get_total_price(order_item) + get_tax(order_item) + get_shipping()
