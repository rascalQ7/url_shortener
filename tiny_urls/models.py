from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from url_shortener import constant


class TinyURL(models.Model):
    id = models.IntegerField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=10)
    original_url = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def linear_congruential_generator(seed):
        modulus = constant.BASE_RANGE_UPPER - constant.BASE_RANGE_LOWER
        lcg = (seed * constant.MULTIPLIER + constant.INCREMENT) % modulus
        new_seed = lcg + constant.BASE_RANGE_LOWER
        return new_seed

    @staticmethod
    def generate_id():
        try:
            latest_record_id = TinyURL.objects.latest('created').id
        except ObjectDoesNotExist:
            latest_record_id = constant.BASE_RANGE_LOWER
        pseudo_random_number = TinyURL.linear_congruential_generator(latest_record_id)
        while TinyURL.objects.filter(pk=pseudo_random_number).exists():
            pseudo_random_number = TinyURL.linear_congruential_generator(latest_record_id + 1)
        return pseudo_random_number

    @staticmethod
    def convert_number_to_base_string(url_id):
        number = url_id
        divider = len(constant.BASE)
        base_string = ''
        while number:
            remainder = number % divider
            base_string += constant.BASE[int(remainder)]
            number //= divider
        return base_string
