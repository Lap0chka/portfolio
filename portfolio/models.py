from django.db import models

class Portfolio(models.Model):
    title = models.CharField(max_length=128)
    is_it = models.CharField(max_length=64, null=True, blank=True, default="")
    description = models.TextField(default='What I used:\nDescription:')
    image = models.ImageField(upload_to='porfolio/midea')
    link = models.URLField(blank=True)
    is_link = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.link:
            self.is_link = True
        super().save(*args, **kwargs)
