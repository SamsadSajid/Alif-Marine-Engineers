"""
This python file will create a flag that will allow
to check in the html file, if there is any review for the product. If
there is, the reviews will be showed. Otherwise,
it will show to write a review.
"""

from django import template
from django.template import Library

register = Library()


@register.assignment_tag()
def check_review_status(product_review):
    value = [p for p in product_review if p.review]
    if value:
        return True
    else:
        return False
