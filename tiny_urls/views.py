from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from .models import TinyURL, TinyURLMETA


def external_redirection(request, tiny_url):
    url = get_object_or_404(TinyURL, name=tiny_url, is_active=True)
    if url.is_valid:
        raise Http404("Tiny url expired")
    original_url = url.original_url
    if url.original_url.lower().startswith('http://'):
        original_url = 'http://' + original_url[6:]
    elif url.original_url.lower().startswith('https://'):
        original_url = 'https://' + original_url[7:]
    else:
        original_url = 'http://' + original_url
    TinyURLMETA.objects.create(tinyURL=url,
                               ip_address=get_client_ip(request),
                               http_referer=get_http_referer(request))
    return redirect(original_url)


def deactivate_tiny_url(request, url_id, redirection):
    url = get_object_or_404(TinyURL, pk=url_id)
    url.is_active = False
    url.save()
    return redirect(redirection)


def get_http_referer(request):
    http_referer = request.META.get('HTTP_REFERER')
    if http_referer is None:
        http_referer = ''
    return http_referer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
