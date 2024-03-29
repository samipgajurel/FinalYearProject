from django.shortcuts import render,redirect
from accounts.models import Profile
import datetime
from .models import Listings
from listings.forms import ListingsImageForm
from django.core.paginator import Paginator
from listings.service import get_latest_products,get_popular_products
from listings.service import get_search_results

# Create your views here.
def index_page (request):
    # Get the index template file absolute path.
    # index_file_path = PROJECT_PATH + '/pages/home.html'
    # Return the index file to client.
    latest_products= get_latest_products()
    paginatorL = Paginator(latest_products, 3)
    page_number_L = request.GET.get('pageL',1)
    page_obj_L = paginatorL.get_page(page_number_L)

    popular_products=get_popular_products()
    paginatorP=Paginator(popular_products,3)
    page_number_P = request.GET.get('pageP',1)
    page_obj_P = paginatorP.get_page(page_number_P)
    return render(request, 'HomePage.html',{'page_obj_L': page_obj_L,
                                            'page_obj_P':page_obj_P})

def add_product (request):
    currentUser= request.user
    role = currentUser.profile.role
    if role == Profile.CONSUMER:
        return render(request,'AccessDenied.html')
    if request.method == "GET":
        form= ListingsImageForm()
        return render(request,'AddPRODUCTPage.html',{'form':form})
    else:
        title = request.POST.get("title")
        description=request.POST.get("description")
        category = request.POST.get("category")
        sub_category = request.POST.get("sub_category")
        now = datetime.datetime.now()
        image = request.FILES.get('picture')
        price = request.POST.get("price")
        unit = request.POST.get("unit")
        featured = request.POST.get("featured")

        print(image)
        listing=Listings(title=title,description=description,creator=currentUser,
                  dateCreated=now,lastModified=now,picture=image,price=price,unit=unit,
                         category=category, sub_category=sub_category, featured=featured)
        listing.save()
        return render(request,'PRODUCTViewPage.html',{'listing':listing})

def fq(text):
    return text.replace(" ","+")
def see_products(request):
    id = request.GET.get('id')
    listing = Listings.objects.get(id=id)
    listing.views = listing.views + 1
    listing.save()
    query = f"{fq(listing.title)}+{fq(listing.category)}+{fq(listing.sub_category)}"
    if not request.GET._mutable:
        request.GET._mutable = True
    request.GET["query"] = query
    request.GET["exclude"] = id
    data = get_search_results(request)
    data['listing'] = listing
    return render(request, 'PRODUCTViewPage.html',data)

def update_products(request):
    currentUser = request.user
    role = currentUser.profile.role
    id = request.GET.get('id')
    print(id)
    listing = Listings.objects.get(id=id)
    if role == Profile.CONSUMER or listing.creator != currentUser:
        return render(request, 'AccessDenied.html')

    if request.method == "GET":
        return render(request, 'UPDATEPage.html', {'listing': listing})
    else:
        listing.title = request.POST.get('title')
        listing.description = request.POST.get("description")
        listing.category = request.POST.get("category")
        listing.sub_category = request.POST.get("sub_category")
        listing.lastModified = datetime.datetime.now()
        image = request.FILES.get('picture')
        listing.unit = request.POST.get('unit')
        listing.price = request.POST.get('price')
        listing.featured = request.POST.get('featured')
        print("#####")
        print(image)
        if image:
            listing.picture = image
        listing.save()
        return render(request, 'PRODUCTViewPage.html', {'listing': listing})

def delete_products(request):
    currentUser = request.user
    role = currentUser.profile.role
    id = request.GET.get('id')
    listing = Listings.objects.get(id=id)
    if role == Profile.CONSUMER or listing.creator != currentUser:
        return render(request, 'AccessDenied.html')

    listing.delete()
    return redirect("/home/")

