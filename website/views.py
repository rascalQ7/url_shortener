from django.shortcuts import render
from django.forms import modelform_factory
from django.core.exceptions import ObjectDoesNotExist
from tiny_urls.models import TinyURL
from url_shortener import constant


def linear_congruential_generator(seed):
    modulus = constant.BASE_RANGE_UPPER - constant.BASE_RANGE_LOWER
    lcg = (seed * constant.MULTIPLIER + constant.INCREMENT) % modulus
    new_seed = lcg + constant.BASE_RANGE_LOWER
    return new_seed


def generate_id():
    try:
        latest_record_id = TinyURL.objects.latest('created').id
    except ObjectDoesNotExist:
        latest_record_id = constant.BASE_RANGE_LOWER
    pseudo_random_number = linear_congruential_generator(latest_record_id)
    while TinyURL.objects.filter(pk=pseudo_random_number).exists():
        pseudo_random_number = linear_congruential_generator(latest_record_id+1)
    return pseudo_random_number


def convert_number_to_base_string(url_id):
    number = url_id
    divider = len(constant.BASE)
    base_string = ''
    while number:
        remainder = number % divider
        base_string += constant.BASE[int(remainder)]
        number //= divider
    return base_string


TinyURLForm = modelform_factory(TinyURL, exclude=['id', 'name', 'created'])


def home(request):
    quick_link = ''
    if request.method == "POST":
        url_id = generate_id()
        id_as_base_string = convert_number_to_base_string(url_id)
        auto_generated_fields = TinyURL(id=url_id, name=id_as_base_string)
        form = TinyURLForm(request.POST, instance=auto_generated_fields)
        if form.is_valid():
            form.save()
            quick_link = constant.DNS + auto_generated_fields.name
    else:
        form = TinyURLForm()
    return render(request, "website/home.html", {"form": form, "quick_link": quick_link})
