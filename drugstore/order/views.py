from django.shortcuts import render, redirect, get_object_or_404
from .forms import CheckoutForm
from store.models import Product
from .models import Order, OrderItem

def checkout_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, quantity in cart.items():
        product = get_object_or_404(Product, id=id)
        product.quantity = quantity
        product.total_price = quantity * product.price
        total += product.total_price
        products.append(product)

    form = CheckoutForm()
    return render(request, 'order/checkout.html', {'products': products, 'total': total, 'form': form})


def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart:cart')

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        return redirect('order:checkout')

    full_name = form.cleaned_data['full_name']
    phone = form.cleaned_data['phone']
    address = form.cleaned_data['address']

    total = 0
    for id, quantity in cart.items():
        product = get_object_or_404(Product, id=id)
        total += product.price * quantity

    order = Order.objects.create(
        user=request.user,
        full_name=full_name,
        phone=phone,
        address=address,
        total=total,
    )

    for id, quantity in cart.items():
        product = get_object_or_404(Product, id=id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
        )

    request.session['cart'] = {}
    return redirect('store:home')
