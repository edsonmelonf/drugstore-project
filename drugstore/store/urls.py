from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('search/', views.search_products, name='search_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart')
]
