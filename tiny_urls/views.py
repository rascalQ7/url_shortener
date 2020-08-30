from django.shortcuts import redirect, get_object_or_404
from .models import TinyURL


def external_redirection(request, tiny_url):
    url = get_object_or_404(TinyURL, name=tiny_url)
    return redirect('http://' + url.original_url)
