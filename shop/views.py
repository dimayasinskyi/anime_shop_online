from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import redirect, HttpResponseRedirect

import stripe
from urllib.parse import urlencode

from .models import Goods, Categories
from user.models import SaveGood, Basket, Comment
from user.forms import CommentForm

# Index
def index(request):
    return render(request, "index.html", {"title": "Anime shop"})

# Catalog and save
def goods(request, mode):
    page_number = int(request.GET.get('page', 1))
    per_page = 4 

    if mode == 'saved' and request.user.is_authenticated:
        goods = Goods.objects.filter(id__in=SaveGood.objects.filter(user=request.user).values_list("good_id", flat=True))
        paginator = Paginator(goods, per_page)
        goods_paginator = paginator.page(page_number)

        good_ids = [good.id for good in goods_paginator]

        goods_with_save_info = [
            {
                "object": good,
                "in_basket": good.id in set(Basket.objects.filter(user=request.user, good_id__in=good_ids).values_list("good_id", flat=True)),
            }
            for good in goods_paginator 
            ]


        context = {
            "title": "Save",
            "goods": goods_with_save_info,
            "page_obj": goods_paginator,
            'save': False,
            'mode': mode,
        }
    else:
        cate = int(request.GET.get('cate', 0))
        query = request.GET.get('find')
        goods = Goods.objects.all().order_by('id')
        if query:
            goods = goods.filter(title__icontains=query).order_by('id')
        if cate:
            goods = goods.filter(category=cate).order_by('id')
            
        paginator = Paginator(goods, per_page)
        goods_paginator = paginator.page(page_number)

        good_ids = [good.id for good in goods_paginator]

        categories = Categories.objects.all()
        if request.user.is_authenticated:

            goods_with_save_info = [
                {
                "object": good,
                "is_saved": good.id in set(SaveGood.objects.filter(user=request.user, good_id__in=good_ids).values_list("good_id", flat=True)),
                "in_basket": good.id in set(Basket.objects.filter(user=request.user, good_id__in=good_ids).values_list("good_id", flat=True)),
                }
            for good in goods_paginator
            ]
        else:
            goods_with_save_info = [{ "object": good } for good in goods_paginator ]
            
        context = {
            "title": "All goods",
            "goods": goods_with_save_info,
            "page_obj": goods_paginator,
            'save': True,
            'mode': mode,
            'categories': categories,
        }
    return render(request, "goods.html", context)

# Good and comment
def single_goods(request, good_id):
    good = get_object_or_404(Goods, pk=good_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=(False))
            obj.user = request.user
            obj.good = good
            obj.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        save = SaveGood.objects.filter(user=request.user, good=good).exists()
        context = {
            'title': good.title,
            "good": good,
            "save": save,
            "in_basket": Basket.objects.filter(user=request.user, good_id=good_id),
            "form": CommentForm(),
            "comments": Comment.objects.filter(good=good_id),

        }
        return render(request, "single_goods.html", context)

# Pay
stripe.api_key = settings.STRIPE_SECRET_KEY
def create_checkout_session(request):
    goods_in_vaskets = Basket.objects.filter(user=request.user)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(good_in_basket.good.price) * 100),
                    'product_data': {
                        'name': good_in_basket.good.title
                    },
                },
                'quantity': good_in_basket.quantity,
                
            }
            for good_in_basket in goods_in_vaskets
        ],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return redirect(session.url, code=303)

def create_checkout_session_good(request, good_id):
    good = Goods.objects.get(id=good_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(good.price) * 100),
                    'product_data': {
                        'name': good.title
                    },
                },
                'quantity': 1,
                
            }
        ],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return redirect(session.url, code=303)
