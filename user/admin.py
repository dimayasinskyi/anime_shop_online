from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Basket, SaveGood


class BasketInline(admin.TabularInline):
    model = Basket
    extra = 0

class SaveGoodInline(admin.TabularInline):
    model = SaveGood
    extra = 0

class UserAdmin(UserAdmin):
    inlines = [BasketInline, SaveGoodInline]


admin.site.register(User, UserAdmin)
