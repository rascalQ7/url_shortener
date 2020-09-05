from django.shortcuts import redirect, get_object_or_404
from .models import TinyURL


def external_redirection(request, tiny_url):
    url = get_object_or_404(TinyURL, name=tiny_url, is_active=True)
    original_url = url.original_url
    if url.original_url.lower().startswith('http://'):
        original_url = 'http://' + original_url[6:]
    elif url.original_url.lower().startswith('https://'):
        original_url = 'https://' + original_url[7:]
    else:
        original_url = 'http://' + original_url
    return redirect(original_url)


def deactivate_tiny_url(request, url_id, redirection):
    url = get_object_or_404(TinyURL, pk=url_id)
    url.is_active = False
    url.save()
    return redirect(redirection)
