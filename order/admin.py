from django.contrib import admin
from .models import Order, OrderGood


class OrderGoodInline(admin.TabularInline):
    model=OrderGood
    extra=1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderGoodInline]

