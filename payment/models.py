from django.db import models
from django.contrib.auth.models import User
from listings.models import Listings
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.TextField(default='Ordered')
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_cancelled= models.DateTimeField(null=True)
    date_delivered= models.DateTimeField(null=True)
    shipping_address=models.TextField(null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Listings,on_delete=models.PROTECT)
    quantity = models.FloatField(default=0)
    rating = models.IntegerField(default=0, null=True)
    review = models.TextField(null=True)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="seller")

    @property
    def subtotal(self):
        return self.quantity*self.product.price

    def __str__(self):
        return f"{self.quantity} {self.product.unit} x {self.product.title}"


