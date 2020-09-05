from django.shortcuts import render, redirect
from django.forms import modelform_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from url_shortener import constant
from tiny_urls.models import TinyURL


TinyURLForm = modelform_factory(TinyURL, exclude=['id', 'name', 'created'])


@login_required
def home(request):
    if request.method == "POST":
        url_id = TinyURL.generate_id()
        id_as_base_string = TinyURL.convert_number_to_base_string(url_id)
        auto_generated_fields = TinyURL(id=url_id, name=id_as_base_string)
        url_form = TinyURLForm(request.POST, instance=auto_generated_fields)
        if url_form.is_valid():
            url_form.save()
            quick_link = constant.DNS + auto_generated_fields.name
    else:
        quick_link = ''
        url_form = TinyURLForm()
    return render(request, "website/home.html", {"url_form": url_form, "quick_link": quick_link})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            validation_message = "Incorrect username or password"
        else:
            login(request, user)
            return redirect(home)
    else:
        validation_message = ''

    return render(request, 'website/login.html', {"validation_message": validation_message})


def logout_user(request):
    logout(request)
    return redirect(login_user)


def sign_up_user(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            validation_message = 'Username already exist'
            return render(request, 'website/signup.html',
                          {"validation_message": validation_message})
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(home)
    validation_message = ''
    return render(request, 'website/signup.html',
                  {"validation_message": validation_message})
