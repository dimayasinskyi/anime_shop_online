from django.shortcuts import render, redirect
from django.urls import reverse

from .form import CheckCorrectOrderForm
from .models import Order
from shop.models import Goods
from user.models import Basket


def check_correct_order(request, good_id):
    if request.method == "POST":
        form = CheckCorrectOrderForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.goods = Goods.objects.get(id=good_id)
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
            obj.goods = Basket.objects.get()
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
    return render(request, 'order/orders.html', )

def order(request, order_id):
    context = {
        'order': Order.objects.get(id=order_id),
    }
    return render(request, 'order/order_detile.html', context)