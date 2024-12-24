from typing import Any

from django.db import models
from django.urls import reverse
from django.utils import timezone
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields
from pytils.translit import slugify


class BlogManager(TranslatableManager):
    """
    Custom manager for the Blog model to retrieve only published blog posts.
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Returns the queryset of published blog posts.

        Returns:
            QuerySet: A queryset filtered by `is_published=True`.
        """
        return super().get_queryset().filter(is_published=True)


class Blog(TranslatableModel):
    """
    A model representing a blog post with translations.

    Attributes:
        translations (TranslatedFields): Translatable fields for the blog post.
        created_at (DateTimeField): The date and time the post was created.
        picture (ImageField): An optional image for the blog post.
        is_published (BooleanField): Indicates if the post is published.
        views (PositiveIntegerField): The number of views for the post.
    """

    translations = TranslatedFields(
        title=models.CharField(max_length=128),
        slug=models.SlugField(max_length=128, blank=True),
        description=models.CharField(max_length=256),
        article=models.TextField(default=""),
    )
    picture = models.ImageField(
        upload_to="blog", null=True, blank=True, default="blog/default.png"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    is_published: models.BooleanField = models.BooleanField(default=True)
    views: models.PositiveIntegerField = models.PositiveIntegerField(default=0)

    # Custom manager to retrieve only published posts
    published = BlogManager()
    # Translatable manager
    objects = TranslatableManager()

    def __str__(self) -> str:
        """
        Returns the string representation of the blog post.

        Returns:
            str: The title of the blog post.
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for the blog post.

        Returns:
            str: The URL to the detail view of the blog post.
        """
        return reverse("detail", args=[self.slug])

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Saves the blog post, generating a slug if it does not exist.

        Args:
            *args (Any): Positional arguments.
            **kwargs (Any): Keyword arguments.
        """
        # Use safe_translation_getter to get the translated field value
        current_slug = self.safe_translation_getter("slug", default=None)
        if not current_slug:
            title = self.safe_translation_getter("title", default="")
            self.slug = slugify(title)
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta options for the Blog model.
        """

        ordering = ["-created_at"]


class Suggest(models.Model):
    """
    A model representing user suggestions or recommendations.

    Attributes:
        title (str): The title of the suggestion.
        description (str): A brief description of the suggestion.
        link (str, optional): An optional URL link related to the suggestion.
    """

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the suggestion.

        Returns:
            str: The title of the suggestion.
        """
        return str(self.title)


class Comment(models.Model):
    """
    A model representing comments on blog posts.

    Attributes:
        post (Blog): The related blog post.
        username (str): The name of the user who made the comment.
        body (str): The content of the comment.
        created_at (datetime): The date and time the comment was created.
        user_id (str): A unique identifier for the user.
    """

    post = models.ForeignKey("Blog", on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Returns the string representation of the comment.

        Returns:
            str: The username and the creation date of the comment.
        """

        return (
            f"{self.username} - "
            f"{timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"
        )
