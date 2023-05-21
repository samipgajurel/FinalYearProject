from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('insufficient-funds/', views.insufficient_funds, name='insufficient_funds'),
]
