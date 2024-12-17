from datetime import datetime, timedelta
from typing import Any


from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from pytils.translit import slugify


class BlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


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
    published = BlogManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

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


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)

    def __str__(self):
        return self.username







