from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

def get_cartitem_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_items = []
        return {"num_cart_items": len(cart_items)}
    else:
        return {"num_cart_items": 0}
