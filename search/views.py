from django.shortcuts import render,redirect
from listings.service import get_search_results



def index_page (request):
    data = get_search_results(request)
    return render(request, 'SearchResults.html',data)
