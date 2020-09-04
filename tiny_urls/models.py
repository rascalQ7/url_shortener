from django.db import models


class TinyURL(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=10)
    original_url = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
