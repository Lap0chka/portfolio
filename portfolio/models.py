from django.db import models

class Portfolio(models.Model):
    title = models.CharField(max_length=128)
   # is_it = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='porfolio/midea')
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title
