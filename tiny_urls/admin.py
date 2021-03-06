from django.contrib import admin
from .models import TinyURL, TinyURLMETA, ConfigItem


admin.site.register(TinyURL)
admin.site.register(TinyURLMETA)


@admin.register(ConfigItem)
class ConfigItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    list_editable = ('value',)
