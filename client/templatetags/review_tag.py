"""
This python file will create a flag that will allow
to check in the html file, if there is any review for the product. If
there is, the reviews will be showed. Otherwise,
it will show to write a review.
"""

from django.template import Library
from officer.models import ProductList
from decimal import getcontext, Decimal
from order.models import Order
from  django.utils.timesince import timesince

register = Library()


# return True if review exists
# return False if no review exists
@register.assignment_tag()
def check_review_status(product_review):
    value = [p for p in product_review if p.review]
    if value:
        return True
    else:
        return False


# return the product name
@register.assignment_tag()
def get_name(item):
    product = ProductList.objects.get(id=item.product_id)
    name = product.product_name
    return name


# return the product description
@register.assignment_tag()
def get_description(item):
    product = ProductList.objects.get(id=item.product_id)
    description = product.product_description
    return description


# return total price for the item, i.e. quantity * each piece price
@register.assignment_tag()
def get_price(item):
    return item.price * item.quantity


# return the total price of all the products of the cart
@register.assignment_tag()
def get_total_price(order_item):
    total = 0
    for item in order_item:
        total += get_price(item)
    return total


# return the tax in %
@register.assignment_tag()
def get_tax_percentage():
    return Decimal(5.00)


# calculate tax on the total price of the cart
@register.assignment_tag()
def get_tax(order_item):
    total = get_total_price(order_item)
    return total * get_tax_percentage()/Decimal(100.00)


# return shipping charge
@register.assignment_tag()
def get_shipping():
    return Decimal(15.00)


# return the total cost including shipping, tax
@register.assignment_tag()
def get_total(order_item):
    return get_total_price(order_item) + get_tax(order_item) + get_shipping()


# return the delivery date of the product set by the Production Manager
@register.assignment_tag()
def get_delivery_date(order):
    _order = Order.objects.get(id=order.id)
    if _order.delivery:
        return _order.delivery
    else:
        return False


# return time of notifications - current time
@register.assignment_tag()
def get_time(time):
    return timesince(time)