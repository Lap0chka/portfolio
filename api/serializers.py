from rest_framework import serializers

from blog.models import Blog
from portfolio.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    """
    Serializer for the Portfolio model.
    Serializes basic fields of the Portfolio model.
    """

    class Meta:
        model = Portfolio
        fields = ["id", "title", "tools", "is_it", "image", "link"]


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blog model with support for translated fields.
    Uses `safe_translation_getter` to fetch translations safely.
    """

    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "article",
            "slug",
            "description",
            "created_at",
            "picture",
        ]

    def get_title(self, obj: Blog) -> str:
        """
        Get the translated title of the blog.

        Args:
            obj (Blog): The Blog instance.

        Returns:
            str: The translated title or an empty string if not available.
        """
        return obj.safe_translation_getter("title", default="")

    def get_slug(self, obj: Blog) -> str:
        """
        Get the translated slug of the blog.

        Args:
            obj (Blog): The Blog instance.

        Returns:
            str: The translated slug or an empty string if not available.
        """
        return obj.safe_translation_getter("slug", default="")

    def get_description(self, obj: Blog) -> str:
        """
        Get the translated description of the blog.

        Args:
            obj (Blog): The Blog instance.

        Returns:
            str: The translated description or an empty string if not available.
        """
        return obj.safe_translation_getter("description", default="")
