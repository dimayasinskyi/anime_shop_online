from django.urls import path

from .views import check_correct_order, check_correct_basket, orders, order


app_name = 'order'
urlpatterns = [
    path('check_correct_order/<int:good_id>/', check_correct_order, name='check_order'),
    path('check_correct_basket/', check_correct_basket, name='check_basket'),
    path('order/list/', orders, name='orders'),
    path('order/<int:order_id>/', order, name='single_order')
]