from django.urls import path

from .views import login_view, logout_view, register_view, profile_view, basket_view, basket_add, add_quantity, subtract_quantity, basket_del, basket_all_del, add_in_save_good, save_goods, delete_comment


app_name = 'user'
urlpatterns = [
    # Authentication
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    # User
    path('profile/', profile_view, name='profile'),
    # Basket
    path('basket/', basket_view, name='basket'),
    path('basket/add/<int:good_id>', basket_add, name='basket_add'),
    path('basket/add_quantity/<int:basket_id>', add_quantity, name="add_quantity"),
    path('basket/subtract_quantity/<int:basket_id>', subtract_quantity, name="subtract_quantity"),
    path('basket/basket_del/<int:basket_id>', basket_del, name="basket_del"),
    path('basket/basket_all_del/', basket_all_del, name="basket_all_del"),
    # Save
    path('save/', save_goods, name="save"),
    path('save/page/<int:page_number>', save_goods, name="paginator"),
    path('save/add/<int:good_id>', add_in_save_good, name="save_add"),
    # Comment
    path('delete/comment/<int:comment_id>', delete_comment, name="delete_comment")
]