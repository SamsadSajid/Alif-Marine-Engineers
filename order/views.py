from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
# import weasyprint
from .models import Order, OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect to the payment
            return redirect('order:success')  # change hobe
        else:
            messages.add_message(request, messages.ERROR,
                                 'Submitted form contains invalid data!')
            return render('order/create.html', {'form': form})
    else:
        if cart:
            form = OrderCreateForm()
            return render(request, 'order/create.html', {'cart': cart,
                                                         'form': form})
        else:
            messages.add_message(request, messages.ERROR,
                                 'Your Cart is Empty. Please Shop with us!')
            return render(request, 'cart/detail.html')


def success(request):
    return render(request, 'order/success.html')
