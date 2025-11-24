from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product

# Create your views here.

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            pid = int(product_id)
            product = Product.objects.get(id=pid)
            product.quantity = quantity
            product.subtotal = product.price * quantity
            total_price += product.subtotal
            products.append(product)
        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    return render(request, 'cart.html', {
        'products': products,
        'total_price': total_price
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart:cart')


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)

        request.session['cart'] = cart
    return redirect('cart:cart')


def checkout_view(request):
    return redirect('order:checkout')
