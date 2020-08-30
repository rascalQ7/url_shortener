from django.shortcuts import redirect
from .models import TinyURL


def external_redirection(request, tiny_url):
    url = TinyURL.objects.get(name=tiny_url)
    return redirect('http://' + url.original_url)
