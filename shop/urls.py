from django.urls import path
from .views import goods, single_good, create_checkout_session, create_checkout_session_good
from django.conf import settings
from django.conf.urls.static import static


app_name = 'shop'
urlpatterns = [
    # Index
    # path('', good, name='goods'),
    # Product
    path('goods/<str:mode>/', goods, name='goods'),
    path('good/<int:good_id>/', single_good, name='single_goods'),
    # Pay
    path('pay/', create_checkout_session, name='pay'),
    path('pay/<int:good_id>/', create_checkout_session_good, name='pay_good'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
