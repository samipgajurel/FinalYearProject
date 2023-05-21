from django.urls import path
from . import views
# When user request home page http://localhost:8000/my_hello_world, it will invoke the home function defined in views.py.
urlpatterns = [
    path('', views.index_page, name='search'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
