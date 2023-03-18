from django.urls import path
from django.contrib.auth.decorators import login_required
# import views from local directory.
from . import views

urlpatterns = [
    # When user request home page http://localhost:8000/my_hello_world, it will invoke the home function defined in views.py.
    path('', views.index_page, name='home'),
    path('add/', login_required(views.add_product),name='add'),
    path('view/',views.see_products,name='view'),
    path("update/",login_required(views.update_products),name='update'),
    path("delete/",login_required(views.delete_products),name='delete'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)