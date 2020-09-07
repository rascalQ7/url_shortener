from unittest import TestCase
from datetime import timedelta
from django.utils import timezone
from django.test import TransactionTestCase
from tiny_urls.models import TinyURL, ConfigItem, TinyURLMETA
from tiny_urls import constant


class TestModelTestCase(TestCase):

    def test_base_converter_returns_unique_string_per_id(self):
        is_all_strings_unique = True
        base_strings_list = []
        for x in range(len(constant.BASE)):
            base_string = TinyURL.convert_number_to_base_string(constant.BASE_RANGE_LOWER + x)
            if base_string in base_strings_list:
                is_all_strings_unique = False
            base_strings_list.append(base_string)
        self.assertTrue(is_all_strings_unique)

    def test_base_converter_generates_same_size_url(self):
        lower = TinyURL.convert_number_to_base_string(constant.BASE_RANGE_LOWER)
        upper = TinyURL.convert_number_to_base_string(constant.BASE_RANGE_UPPER)
        self.assertTrue(len(lower) == len(upper))


class TaskModelTransactionTestCase(TransactionTestCase):
    fixtures = ['tiny_urls/fixtures/unit-tests.json']

    def setUp(self):
        self.urls_expires_in = ConfigItem.objects.get(name='url_expiration_period_in_seconds').value
        self.urls_redirection_limit = ConfigItem.objects.get(name='redirection_limit').value

    def test_fixtures_load(self):
        self.assertTrue(TinyURL.objects.count() > 0)

    def test_url_is_not_valid_if_expired(self):
        url = TinyURL()
        url.created = timezone.now() - timedelta(seconds=self.urls_expires_in + 1)
        url.is_active = True
        self.assertFalse(url.is_valid)

    def test_url_is_not_valid_if_deactivated(self):
        url = TinyURL()
        url.created = timezone.now()
        url.is_active = False
        self.assertFalse(url.is_valid)

    def test_url_is_not_valid_if_breached_redirection_limit(self):
        meta = TinyURLMETA.objects.get(pk=1)
        url = meta.tiny_url
        url.created = timezone.now()
        url.active = True
        meta.id += 1
        for meta.id in range(self.urls_redirection_limit + 1):
            meta.save()
        self.assertFalse(url.is_valid)

    def test_url_is_valid_if_all_conditions_are_true(self):
        url = TinyURL()
        url.created = timezone.now()
        url.is_active = True
        self.assertTrue(url.is_valid)
