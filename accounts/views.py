from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm,ProfileForm
from django.shortcuts import render, redirect
from .models import Profile
from django.core.paginator import Paginator
from listings.service import get_latest_products_by_user,get_featured_products_by_user
from payment.service import get_order_for_seller,get_order_for_consumer
from django.contrib.auth.models import User

# Create your views here.
def dashboard_page (request):
    # Get the index template file absolute path.
    # index_file_path = PROJECT_PATH + '/pages/Home.html'
    # Return the index file to client.
    currentUser= request.user
    account= Profile.objects.get(user=currentUser)
    print(account.first_name)
    latest_products_by_user = get_latest_products_by_user(currentUser)
    paginatorL = Paginator(latest_products_by_user, 6)
    page_number_L = request.GET.get('pageL', 1)
    page_obj_L = paginatorL.get_page(page_number_L)
    featured_product_by_user = get_featured_products_by_user(currentUser)
    paginatorF = Paginator(featured_product_by_user, 3)
    page_number_F = request.GET.get('pageF', 1)
    page_obj_F = paginatorF.get_page(page_number_F)

    if account.role != Profile.CONSUMER:
        orders= get_order_for_seller(currentUser)
    else:
        orders = get_order_for_consumer(currentUser)
    paginatorO = Paginator(orders, 6)
    page_number_O = request.GET.get('pageO', 1)
    page_obj_O = paginatorO.get_page(page_number_O)
    return render(request, 'UserDashboard.html', {"account": account,
                                                  'page_obj_L': page_obj_L,
                                                  'page_obj_F': page_obj_F,
                                                  'page_obj_O': page_obj_O})
def profile_page(request):
    next = "/accounts/dashboard/"
    user = request.user
    profile= Profile.objects.get(user=user)
    print(user)
    if request.method == "GET":
        form= ProfileForm(instance=profile)
    else:
        form = ProfileForm(request.POST,instance=profile)
        print(form)
        if form.is_valid():
            user.refresh_from_db()
            if user.profile is None:
                print('profileMissing')

                profile = Profile(user=user,
                                  first_name=form.cleaned_data.get('first_name'),
                                  last_name=form.cleaned_data.get('last_name'),
                                  email=form.cleaned_data.get('email'),)
                profile.save()
                # user.profile= profile
                # user.save()
            else:
                print(user.profile.first_name,form.cleaned_data.get('first_name'))
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')
                user.profile.phone = form.cleaned_data.get('phone')
                image = request.FILES.get('picture')
                if image:
                    user.profile.picture= image
                user.profile.save()
                user.save()
            return redirect(next)

    return render(request, 'EditProfile.html', {"form": form,"next":next,'model':user.profile})






def signup_page(request):
    if request.method == "GET":
        form= SignUpForm()
    else:
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.role = form.cleaned_data.get('role')
            user.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect('/accounts/login/')
    return render(request, 'SignUp.html', {'form': form})



