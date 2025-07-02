from django.urls import path
from .views import goods, single_goods, create_checkout_session, create_checkout_session_good
from django.conf import settings
from django.conf.urls.static import static


app_name = 'shop'
urlpatterns = [
    # Index
    path('', goods, name='goods'),
    # Product
    path('good/<int:good_id>/', single_goods, name='single_goods'),
    path('goods/<str:mode>/', goods, name='goods'),
    # Pay
    path('pay/', create_checkout_session, name='pay'),
    path('pay/<int:good_id>', create_checkout_session_good, name='pay_good'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
