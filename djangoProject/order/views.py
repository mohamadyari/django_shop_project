from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
from .forms import *
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
import requests
import json
from zeep import Client
from django.utils.crypto import get_random_string
import ghasedak
from django.core.mail import EmailMessage

# Create your views here.


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    context = {'order': order, 'form': form}
    return render(request, 'order/order.html', context)


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.create(user_id=request.user.id, email=data['email'], first_name=data['first_name'],
                                         last_name=data['last_name'], address=data['address'], code=code)
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=c.product_id,
                                         variant_id=c.variant_id, quantity=c.quantity)
            
            return redirect('order:order_detail', order.id)


@require_POST
def coupon_order(request, order_id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'this code wrong')
            return redirect('order:order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('order:order_detail', order_id)

MERCHANT = ''
# amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional

client = Client('')
CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for realy server.


def send_request(request, price, order_id):
    global amount
    # id = order_id
    amount = price
    result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('' +
                        str(result.Authority))
    else:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()

        cart = ItemOrder.objects.filter(order_id=order_id)
        for c in cart:
            product = Product.objects.get(id=c.product.id)
            product.sell += c.quantity
            product.save()

            phone = f"0{request.user.profile.phone}"

            sms = ghasedak.Ghasedak("")
            sms.send({'message':, '': phone, '': ""})

        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT,
                                                    request.GET['Authority'],
                                                    amount)
        if result.Status == 100:
           
            return HttpResponse('Transaction success.\nRefID: ' +
                                str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' +
                                str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' +
                                str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')

