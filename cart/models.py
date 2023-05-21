from django.db import models
from django.contrib.auth.models import User
from listings.models import Listings

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Listings, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.quantity*self.product.price

    def __str__(self):
        return f"{self.quantity} {self.product.unit} x {self.product.title}"


