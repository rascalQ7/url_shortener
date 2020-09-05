from django.urls import path
from tiny_urls.views import external_redirection, deactivate_tiny_url

urlpatterns = [
    path('deactivate/<int:url_id>/?next=<str:redirection>', deactivate_tiny_url, name='deactivate'),
    path('<str:tiny_url>', external_redirection),
]
