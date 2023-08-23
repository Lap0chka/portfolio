from django.db import models
from tinymce.models import HTMLField

class Blog(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    arrticle = models.TextField(default="")
    data = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

class Suggest(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
