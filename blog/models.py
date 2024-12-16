from django.db import models
from django.shortcuts import redirect
from pytils.translit import slugify
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify


class Blog(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=128),
        slug=models.SlugField(max_length=128, blank=True),
        description=models.CharField(max_length=256),
        article=models.TextField(default="")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='blog', null=True, blank=True, default='blog/default.png')
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return redirect('detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']



class Suggest(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
