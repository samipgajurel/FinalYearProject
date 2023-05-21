from django.shortcuts import render
from listings.service import get_latest_products,get_popular_products
from django.core.paginator import Paginator

# Create your views here.
def index_page (request):
    latest_products = get_latest_products()
    paginatorL = Paginator(latest_products, 6)
    page_number_L = request.GET.get('pageL', 1)
    page_obj_L = paginatorL.get_page(page_number_L)

    popular_products = get_popular_products()
    paginatorP = Paginator(popular_products, 6)
    page_number_P = request.GET.get('pageP', 1)
    page_obj_P = paginatorP.get_page(page_number_P)
    return render(request, 'HomePage.html', {'page_obj_L': page_obj_L,
                                             'page_obj_P': page_obj_P})



