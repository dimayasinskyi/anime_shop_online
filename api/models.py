from shop.models import Good
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .authentication import CustomAuthentication


class GoodResource(ModelResource):
    class Meta:
        queryset = Good.objects.all()
        resource_name = 'goods'
        allowed_methods = ['get', 'post', 'delete']
        authentication = CustomAuthentication()
        authorization = Authorization()

    def dehydrate_title(self, bundle):
        return bundle.data['title'].upper()

