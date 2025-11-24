from django.shortcuts import render, redirect
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def search_products(request):

    query = request.GET.get('q', '').strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name_product__icontains=query) | Q(description__icontains=query)
    ).distinct()

    
    context_search = {
        'query': query,
        'products': products,

    }

    return render(request, 'store/home.html', context_search)



@login_required
def go_to_cart(request):
    return redirect('cart:cart_view')



def add_to_cart(request, product_id):

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1 

    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('store:home')