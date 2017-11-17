from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# the following model will move to shop/models
from officer.models import ProductList
from django.contrib.auth.decorators import login_required
from user_group.check_group import group_required
from .cart import Cart
from .forms import CartAddProductForm


@login_required
@group_required('client_group')
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductList, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductList, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
