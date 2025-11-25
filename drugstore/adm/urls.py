from django.urls import path
from . import views

app_name = 'adm'

urlpatterns = [
    path('dashboard/', views.adm_dashboard, name='dashboard'),
]