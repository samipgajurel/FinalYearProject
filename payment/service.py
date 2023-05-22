from .models import Order, OrderItem

def get_order_for_seller(seller, limit=15):
    orders= OrderItem.objects.filter(seller= seller)[:limit]
    return orders

def get_order_for_consumer(user, limit=15):
    orders = OrderItem.objects.select_related("order").filter(order__user=user)[:limit]
    return orders