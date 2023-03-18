from django.urls import path
from django.contrib.auth.decorators import login_required
# import views from local directory.
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
 # When user request home page http://localhost:8000/my_hello_world, it will invoke the home function defined in views.py.
 #    path('', login_required(views.dashboard_page), name='dashboard'),
    path('', views.signup_page, name='signup'),
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', login_required(views.dashboard_page), name='dashboard'),
    path('profile/',login_required(views.profile_page),name='profile'),
]
