from django.contrib import admin
from .models import TinyURL, TinyURLMETA, ConfigItem


admin.site.register(TinyURL)
admin.site.register(TinyURLMETA)
admin.site.register(ConfigItem)
