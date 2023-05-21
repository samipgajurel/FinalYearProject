from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listings.models import Listings

@login_required
def view_cart(request):
    # Retrieve the current cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Retrieve the cart items associated with the current cart
    cart_items = CartItem.objects.filter(cart=cart)
    # Calculate the total price of the cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request):
    product_id = request.GET.get('id')
    # Retrieve the product that the user wants to add to the cart
    product = get_object_or_404(Listings, id=product_id)
    # Retrieve the current cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    quantity = request.POST.get("quantity")
    if not created:
        # Increment the quantity of the cart item if the product is already in the cart
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'The product was successfully added to your cart.')
    else:
        # Set the quantity of the cart item to 1 if the product is not in the cart
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'The product was successfully added to your cart.')
    return redirect('view_cart')

@login_required
def remove_from_cart(request):
    cart_item_id = request.GET.get('id')
    # Retrieve the cart item that the user wants to remove
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, 'The product was successfully removed from your cart.')
    return redirect('view_cart')

