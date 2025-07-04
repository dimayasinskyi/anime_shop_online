from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shop.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('shop/', include('shop.urls')),
    path('api/', include('api.urls')),
    path('user/', include('user.urls')),
    path('order/', include('order.urls')),
    path("auth/", include("social_django.urls", namespace="social")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)