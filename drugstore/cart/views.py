from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product


# Create your views here.
def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for id, quantity in cart.items():
        product = get_object_or_404(Product, id=id)
        product.quantity = quantity
        product.total_price = quantity * product.price
        total_price += product.total_price
        products.append(product)

    return render(request, 'cart.html', {
        'products': products,
        'total_price': total_price,
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')


def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')


def checkout_view(request):
    return redirect('order:checkout')