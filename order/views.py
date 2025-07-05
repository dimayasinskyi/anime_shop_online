from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CheckCorrectOrderForm
from .models import Order, OrderGood
from shop.models import Good
from user.models import Basket


def check_correct_order(request, good_id):
    if request.method == "POST":
        form = CheckCorrectOrderForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            OrderGood.objects.create(order=obj, good=Good.objects.get(id=good_id), quantity=1)
            return redirect('shop:pay_good', good_id=good_id)
    else:
        good = Good.objects.get(id=good_id)
        context = {
            'title': 'Check correct order',
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

def check_correct_basket(request):
    if request.method == "POST":
        form = CheckCorrectOrderForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            for basket_good in Basket.objects.all():
                OrderGood.objects.create(order=obj, good=basket_good.good, quantity=basket_good.quantity)
            return redirect('shop:pay')
    else:
        basket = Basket.objects.filter(user=request.user)
        context = {
            'title': 'Check correct basket',
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
    orders = Order.objects.filter(user=request.user)
    context = {
        'title': 'My orders',
        'orders_on_hold_new': orders.filter(status__in=['new', 'on_hold']).order_by('-id'),
        'orders_processing': orders.filter(status='processing').order_by('-id'),
        'orders_shipped': orders.filter(status='shipped').order_by('-id'),
        'orders_delivered': orders.filter(status='delivered').order_by('-id'),
        'orders_cancelled_returned_failed': orders.filter(status__in=['cancelled', 'returned', 'failed']).order_by('-id'),
    }
    return render(request, 'order/order_list.html', context)

def order(request, order_id):
    context = {
        'title': 'Detile order',
        'order': Order.objects.get(id=order_id),
    }
    return render(request, 'order/order_detile.html', context)