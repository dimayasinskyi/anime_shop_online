from django.shortcuts import render

from shop.models import Good
from tastypie.resources import ModelResource


class GoodResource(ModelResource):
    class Meta:
        queryset = Good.objects.all()
        resource_name = 'good'
        allowed_methods = ['get']

