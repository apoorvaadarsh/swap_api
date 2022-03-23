from django.db import models

class Swap(models.Model):
    image_url = models.CharField(max_length=200)
    signature_url = models.CharField(max_length=200)

    def __str__(self):
        return self.image_url
