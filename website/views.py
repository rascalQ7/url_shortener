from django.shortcuts import render, redirect
from django.forms import modelform_factory

from tiny_urls.models import TinyURL


TinyURLForm = modelform_factory(TinyURL, exclude=[TinyURL.name])


def home(request):
    if request.method == "POST":
        form = TinyURLForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TinyURLForm()
    return render(request, "website/home.html", {"form": form})
