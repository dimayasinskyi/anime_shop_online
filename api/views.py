from django.shortcuts import render

from shop.models import Goods
from tastypie.resources import ModelResource


class GoodsResource(ModelResource):
    class Meta:
        queryset = Goods.objects.all()
        resource_name = 'goods'
        allowed_methods = ['get']

