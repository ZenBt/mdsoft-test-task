"""mdsoft_test_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from rest_framework.routers import SimpleRouter

from city_info.views import CityView, StreetView
from shop_info.views import ShopView

# router = SimpleRouter()

# router.register(r'city', CityViewSet)
# router.register(r'city/street/<int:city_id>', StreetViewSet, basename='Street')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('city/', CityView.as_view(), name='city'),
    path('city/street/<int:city_id>', StreetView.as_view(), name='street'),
    path('shop/', ShopView.as_view(), name='shop')]

# urlpatterns += router.urls