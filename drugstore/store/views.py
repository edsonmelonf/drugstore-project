from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


# Create your views here.

def home_view(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

