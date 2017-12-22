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
from notifications.signals import notify
from authentication.models import Employee, User, Profile, Client


def order_create(request):
    user = request.user
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            _email = form.cleaned_data['email']
            print (_email)
            print (user.email)
            if _email != user.email:
                print ("error")
                messages.add_message(request, messages.ERROR,
                                     "Your email doesn't match. Please provide the email you used"
                                     "to open this account")
                return render(request, 'order/create.html', {'form': form})
            else:
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
            # generate notification for production manager
                msg = "A new order has been added by user {0}".format(user.profile.get_screen_name())
                # profile = Employee.objects.filter(user=)
                # _recipient = Employee.objects.filter(user=User.objects.filter(profile__account_type=3))
                _recipient = User.objects.filter(profile__account_type=3)
                print ("notify to ")
                print(_recipient)
                notify.send(user, recipient=list(_recipient), verb=msg, action_object=order)
            # redirect to the payment
                return redirect('client:order_view', pk=order.id)  # change hobe(-->hoise)
        else:
            messages.add_message(request, messages.ERROR,
                                 'Submitted form contains invalid data!')
            return render(request, 'order/create.html', {'form': form})
    else:
        if cart:
            form = OrderCreateForm(instance=user, initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            })
            return render(request, 'order/create.html', {'cart': cart,
                                                         'form': form})
        else:
            messages.add_message(request, messages.ERROR,
                                 'Your Cart is Empty. Please Shop with us!')
            return render(request, 'cart/detail.html')


def success(request):
    return render(request, 'order/success.html')
