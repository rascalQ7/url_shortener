from django.test import TestCase
from tiny_urls.models import TinyURL
from url_shortener import constant


class TestViews(TestCase):

    def test_base_converter_returns_unique_string_per_id(self):
        is_all_strings_unique = True
        base_strings_list = []
        for x in range(len(constant.BASE)):
            base_string = TinyURL.convert_number_to_base_string(constant.BASE_RANGE_LOWER + x)
            if base_string in base_strings_list:
                is_all_strings_unique = False
            base_strings_list.append(base_string)
        assert is_all_strings_unique

    def test_base_converter_generates_same_size_url(self):
        lower = TinyURL.convert_number_to_base_string(constant.BASE_RANGE_LOWER)
        upper = TinyURL.convert_number_to_base_string(constant.BASE_RANGE_UPPER)
        assert len(lower) == len(upper)
