from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),

]