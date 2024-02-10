"""
URL configuration for first_django_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myapp.views import welcome, hello_world, profile_view, get_profile_by_name, update_email, profile_detail_view, product_view, product_detail_view, products_by_price_desc, products_in_price_range, products_recently_added, products_by_keyword, products_by_category

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),
    path('hello/', hello_world, name='hello_world'),
    path('profiles/', profile_view, name='profiles'),
    path('profiles/<int:pk>/', profile_detail_view, name='profile_detail'),
    path('profile/<str:name>/', get_profile_by_name, name='get_profile_by_name'),
    path('profile/<str:name>/email/', update_email, name='update_email'),
    path('products/', product_view, name='products'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('products/ordered-by-price/', products_by_price_desc, name='ordered_products'),
    path('products/in-price-range-<int:min_price>-<int:max_price>/', products_in_price_range,
         name='price_range_products'),
    path('products/recently-added/', products_recently_added, name='recent_products'),
    path('products/by-keyword-<str:keyword>/', products_by_keyword, name='keyword_products'),
    path('products/by-category-<str:category>/', products_by_category, name='category_products')
]
