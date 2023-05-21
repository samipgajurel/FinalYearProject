from .models import Listings
from datetime import datetime, timedelta
# from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator

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

#get latest product by user
def get_latest_products_by_user(user, limit=15):
    latest= Listings.objects.filter(creator=user).order_by('-dateCreated')[:limit]
    return latest

def get_featured_products_by_user(user, limit=15):
    featured = Listings.objects.filter(creator=user,featured=1).order_by('-dateCreated')[:limit]
    return featured

def get_searched_products(query,limit=15,exclude=None):
    tokens = query.split("+")

    filter = None
    for token in tokens:
        if filter is None:
            filter = Q(title__icontains=token)| Q(description__icontains=token)| Q(category__icontains=token)| Q(sub_category__icontains=token)
        else:
            filter = filter|Q(title__icontains=token)| Q(description__icontains=token)| Q(category__icontains=token)| Q(sub_category__icontains=token)
    if exclude is not None:
        filter = ~Q(id=exclude)&filter
    products= Listings.objects.filter(filter).order_by('-dateCreated')[:limit]
    return products

def get_search_results(request):
    query = request.GET.get('query')
    exclude = request.GET.get('exclude',None)
    search_products = get_searched_products(query,exclude=exclude)
    paginatorS = Paginator(search_products, 6)
    page_number_S = request.GET.get('pageS', 1)
    page_obj_S = paginatorS.get_page(page_number_S)
    return  {'page_obj_S': page_obj_S,"query":query}