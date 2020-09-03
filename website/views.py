from django.shortcuts import render
from django.forms import modelform_factory
import random
from tiny_urls.models import TinyURL
from url_shortener import constant


def get_random_id():
    random_id = random.randint(constant.BASE_62_100000, constant.BASE_62_ZZZZZZ)
    while TinyURL.objects.filter(pk=random_id).exists():
        random_id = random.randint(constant.BASE_62_100000, constant.BASE_62_ZZZZZZ)
    return random_id


def id_to_base62_string(id):
    return id


TinyURLForm = modelform_factory(TinyURL, exclude=['id', 'name'])


def home(request):
    if request.method == "POST":
        random_id = TinyURL(id=get_random_id())
        form = TinyURLForm(instance=random_id, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TinyURLForm()
    return render(request, "website/home.html", {"form": form})
