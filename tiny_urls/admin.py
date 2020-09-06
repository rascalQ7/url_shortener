from django.contrib import admin
from .models import TinyURL, TinyURLMETA


admin.site.register(TinyURL)
admin.site.register(TinyURLMETA)
