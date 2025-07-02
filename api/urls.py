from django.urls import path, include
from api.models import GoodsResource
from tastypie.api import Api

goodsresource = GoodsResource()

api = Api(api_name='v1')
api.register(goodsresource)


app_name='api'
urlpatterns = [
    path('', include(api.urls), name='api')
]