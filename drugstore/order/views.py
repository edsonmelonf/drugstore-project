from django.shortcuts import render, redirect, get_object_or_404
from .forms import CheckoutForm
from store.models import Produto
from .models import Order, OrderItem

def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart:cart')

    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Produto, id=product_id)
        product.quantity = quantity
        product.total_price = product.price * quantity
        total += product.total_price
        products.append(product)

    form = CheckoutForm()
    return render(
        request,
        'checkout.html',
        {
            'products': products,
            'total': total,
            'form': form
        }
    )

def place_order(request):

    if request.method != 'POST':
        return redirect('cart:cart')

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
    for product_id, quantity in cart.items():
        product = get_object_or_404(Produto, id=product_id)
        total += product.price * quantity

    order = Order.objects.create(
        user=request.user,
        full_name=full_name,
        phone=phone,
        address=address,
        total=total
    )

    for product_id, quantity in cart.items():
        product = get_object_or_404(Produto, id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    request.session['cart'] = {}
    return redirect('store:home')
