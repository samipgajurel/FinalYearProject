from .models import Listings
from datetime import datetime, timedelta
# from django.contrib.auth.models import User

def get_total_products():
    return Listings.objects.count()
# def get_total_admins():
#     return User.objects.filter(is_superuser=True).count()
def get_products_this_week():
    now = datetime.now()
    last_week= now -timedelta(days=7)
    return Listings.objects.filter(dateCreated__gte=last_week).count()

def get_latest_products(limit=15):
    latest= Listings.objects.all().order_by('-dateCreated')[:limit]
    return latest

def get_popular_products(limit=15):
    popular= Listings.objects.all().order_by('-views')[:limit]
    return popular

