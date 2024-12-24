from typing import Dict, Optional

from django.contrib import admin
from django.http import HttpRequest
from parler.admin import TranslatableAdmin

from blog.models import Blog, Comment, Suggest


@admin.register(Blog)
class BlogAdmin(TranslatableAdmin):
    """
    Admin class for the Blog model with translation support.
    """

    list_display = ("title", "slug", "created_at", "is_published", "views")
    list_filter = ("is_published", "created_at")
    search_fields = ("translations__title", "translations__slug")
    readonly_fields = ("views", "created_at")
    ordering = ("-created_at",)

    def get_prepopulated_fields(
        self, request: HttpRequest, obj: Optional[object] = None
    ) -> Dict[str, tuple]:
        """
        Automatically populate the slug field based on the title.
        """
        return {"slug": ("title",)}


@admin.register(Suggest)
class SuggestAdmin(admin.ModelAdmin):
    """
    Admin class for the Suggest model.
    """

    list_display = ("title", "description", "link")
    search_fields = ("title", "description")
    list_filter = ("title",)
    ordering = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin class for the Comment model.
    """

    list_display = ("username", "post", "created_at")
    list_filter = ("created_at", "post")
    search_fields = ("username", "body", "post__translations__title")
    readonly_fields = ("created_at", "user_id")
    ordering = ("-created_at",)
