from django.db import models


class TinyURL(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    original_url = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
