from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import BlogSerializer, PortfolioSerializer
from blog.models import Blog
from portfolio.models import Portfolio


class PortfolioListView(APIView):
    """
    API endpoint for retrieving the list of portfolio items.
    """

    permission_classes = [AllowAny]

    def get(
        self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        """
        Handle GET requests to retrieve all portfolio items.

        Args:
            request: The HTTP request.

        Returns:
            Response: JSON serialized list of portfolio items.
        """
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)


class BlogListView(APIView):
    """
    API endpoint for retrieving the list of published blog posts.
    """

    permission_classes = [AllowAny]

    def get(
        self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        """
        Handle GET requests to retrieve all published blog posts.

        Args:
            request: The HTTP request.

        Returns:
            Response: JSON serialized list of published blog posts.
        """
        blogs = Blog.published.all()
        serializer = BlogSerializer(blogs, many=True)
        data = serializer.data

        for item in data:
            item.pop("article", None)

        return Response(serializer.data)


class BlogDetailView(APIView):
    """
    API endpoint for retrieving details of a single blog post.
    """

    permission_classes = [AllowAny]

    def get(
        self,
        request: Request,
        slug: str,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Handle GET requests to retrieve details of a single blog post.

        Args:
            request: The HTTP request.
            slug: The slug of the blog post.

        Returns:
            Response: JSON serialized details of the blog post.
        """
        language = request.LANGUAGE_CODE

        post = get_object_or_404(
            Blog,
            translations__language_code=language,
            translations__slug=slug,
        )
        serializer = BlogSerializer(post)
        return Response(serializer.data)
