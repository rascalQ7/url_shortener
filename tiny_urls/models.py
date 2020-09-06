from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.utils import timezone
from tiny_urls import constant


class TinyURL(models.Model):
    id = models.IntegerField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=10, db_index=True)
    original_url = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_expired(self):
        expires_in = ConfigItem.objects.get(name='url_expiration_period_in_seconds')
        return self.created < timezone.now() - timedelta(seconds=expires_in.value)

    def is_above_redirection_limit(self):
        redirection_limit = ConfigItem.objects.get(name='redirection_limit')
        return TinyURLMETA.objects.filter(tinyURL=self).count() <= redirection_limit.value

    @property
    def is_valid(self):
        return not self.is_expired() \
               or not self.is_above_redirection_limit() \
               and not self.is_active

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


class TinyURLMETA(models.Model):
    tinyURL = models.ForeignKey(TinyURL, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15)
    http_referer = models.TextField(blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)


class ConfigItem(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return self.name
