from django.urls import path
from .views import cart_view, update_cart, remove_from_cart, checkout_view, add_to_cart


app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart'),
    path('update/<int:product_id>/', update_cart, name='update_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),

]
