from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .forms import RegisterForm, UserProfileForm
from shop.models import Good
from .models import Basket, SaveGood, Comment

# Register, login in and logout
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))

    else:
        form = RegisterForm()

    context = {
        "title": "Registrasion",
        "form": form,
    }
    return render(request, "register.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("index"))
    else:
        form = AuthenticationForm()

    context = {
        "title": "Login",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")

# User
@login_required()
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user:profile"))
        else:
            print(form.errors)
    
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "title": "Profile",
        "form": form,
    }
    
    return render(request, "profile.html", context)

# Basket
@login_required()
def basket_add(request, good_id):
    good = Good.objects.get(id=good_id)
    baskets = Basket.objects.filter(user=request.user, good=good)

    if not baskets.exists():
        Basket.objects.create(user=request.user, good=good, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1 
        baskets.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required()
def basket_view(request):
    try:
        sum = Basket.objects.last().sum()
    except:
        sum = None
        
    context = {
        "title": "Basket",
        "baskets": Basket.objects.filter(user=request.user),
        "sum": sum,
        "total_sum": Basket.objects.filter(user=request.user).total_sum(),
    }
    return render(request, "user/basket.html", context)


def add_quantity(request, basket_id):
    basket_qt = Basket.objects.get(id=basket_id)
    basket_qt.quantity += 1
    basket_qt.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def subtract_quantity(request, basket_id):
    basket_qt = Basket.objects.get(id=basket_id)
    if basket_qt.quantity > 1:
        basket_qt.quantity -= 1
        basket_qt.save()
    else:
        basket_qt.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def basket_del(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def basket_all_del(request):
    basket = Basket.objects.all()
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

# Save
def save_goods(request, page_number=1):
    goods = SaveGood.objects.all()

    per_page = 4
    paginator = Paginator(goods, per_page)
    paginator_good = paginator.page(page_number)
    context = {
        "title": "Save",
        "goods": paginator_good
    }
    return render(request, "user/save.html", context)


@login_required()
def add_in_save_good(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    if not SaveGood.objects.filter(user=request.user, good=good).exists():
        save = SaveGood.objects.create(user=request.user, good=good)
        save.save()
    else:
        SaveGood.objects.filter(user=request.user, good=good).delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

# Comment 
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])