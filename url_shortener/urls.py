from django.contrib import admin
from django.urls import path
from website.views import home
from tiny_urls.views import external_redirection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('<str:tiny_url>', external_redirection),
]
