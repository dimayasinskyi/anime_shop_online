from django.urls import path, include
from api.models import GoodResource
from tastypie.api import Api

goodresource = GoodResource()

api = Api(api_name='v1')
api.register(goodresource)


app_name='api'
urlpatterns = [
    path('', include(api.urls), name='api')
]