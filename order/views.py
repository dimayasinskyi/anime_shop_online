from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CheckCorrectOrderForm
from .models import Order
from shop.models import Goods
from user.models import Basket


def check_correct_order(request, good_id):
    if request.method == "POST":
        form = CheckCorrectOrderForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('shop:pay_good', good_id=good_id)
    else:
        good = Goods.objects.get(id=good_id)
        context = {
            'form': CheckCorrectOrderForm(initial={
                'state': request.user.state,
                'address': request.user.address,
                'city': request.user.city,
                'zip': request.user.zip,
            }),
            'good': good,
            'total_sum': good.price,
            'pay': reverse('shop:pay_good', kwargs={'good_id': good_id})
        } 
        return render(request, 'order/check_order.html', context)

def check_correct_basketr(request):
    if request.method == "POST":
        form = CheckCorrectOrderForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('shop:pay')
    else:
        basket = Basket.objects.filter(user=request.user)
        context = {
            'form': CheckCorrectOrderForm(initial={
                'state': request.user.state,
                'address': request.user.address,
                'city': request.user.city,
                'zip': request.user.zip,
            }),
            'goods': basket,
            'total_sum': basket.total_sum(),
        } 
        return render(request, 'order/check_order.html', context)


def orders(request):
    orders = Order.objects.all()
    context = {
        'order_new': orders.filter(status='new'),
        'order_processing': orders.filter(status='processing'),
        'order_shipped': orders.filter(status='shipped'),
        'order_on_hold': orders.filter(status='on_hold'),
        'order_cancelled': orders.filter(status='delivered'),
        'order_returned': orders.filter(status='cancelled'),
        'order_failed': orders.filter(status='failed'),
    }
    return render(request, 'order/order_list.html', )

def order(request, order_id):
    context = {
        'order': Order.objects.get(id=order_id),
    }
    return render(request, 'order/order_detile.html', context)