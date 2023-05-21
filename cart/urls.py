from django.urls import path
from .views import add_to_cart, remove_from_cart, view_cart

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/', remove_from_cart, name='remove_from_cart'),
]
