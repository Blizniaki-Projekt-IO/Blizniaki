from django.db import models


class Face(models.Model):
    image = models.ImageField(upload_to="faces")
    raport_url = models.CharField(max_length=256)
