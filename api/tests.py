from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Blog
from portfolio.models import Portfolio


class PortfolioAPITestCase(APITestCase):
    """
    Test cases for the Portfolio API endpoints.
    """

    def setUp(self) -> None:
        """
        Set up test data for portfolio API tests.
        """
        self.portfolio1 = Portfolio.objects.create(
            title="Portfolio 1", tools="Django, React", is_it="Web Development"
        )
        self.portfolio2 = Portfolio.objects.create(
            title="Portfolio 2", tools="Flask, Vue", is_it="Backend"
        )

    def test_get_portfolio_list(self) -> None:
        """
        Test that the portfolio list endpoint returns all portfolios.
        """
        response = self.client.get(reverse("portfolio-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Portfolio 1")

    def test_post_portfolio_list_not_allowed(self) -> None:
        """
        Test that POST requests to the portfolio list endpoint are not allowed.
        """
        response = self.client.post(reverse("portfolio-list"), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class BlogAPITestCase(APITestCase):
    """
    Test cases for the Blog API endpoints.
    """

    def setUp(self) -> None:
        """
        Set up test data for blog API tests.
        """
        self.blog1 = Blog.objects.create(
            title="Blog 1", slug="blog-1", is_published=True
        )
        self.blog2 = Blog.objects.create(
            title="Blog 2", slug="blog-2", is_published=False
        )

    def test_get_blog_list(self) -> None:
        """
        Test that the blog list endpoint returns only published blogs.
        """
        response = self.client.get(reverse("blog-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only published blogs
        self.assertEqual(response.data[0]["title"], "Blog 1")

    def test_post_blog_list_not_allowed(self) -> None:
        """
        Test that POST requests to the blog list endpoint are not allowed.
        """
        response = self.client.post(reverse("blog-list"), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_blog_detail(self) -> None:
        """
        Test that the blog detail endpoint returns the correct blog details.
        """
        response = self.client.get(reverse("blog-detail", kwargs={"slug": "blog-1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Blog 1")

    def test_get_blog_detail_not_found(self) -> None:
        """
        Test that the blog detail endpoint returns 404 for non-existent blogs.
        """
        response = self.client.get(
            reverse("blog-detail", kwargs={"slug": "nonexistent-blog"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_blog_detail_not_allowed(self) -> None:
        """
        Test that POST requests to the blog detail endpoint are not allowed.
        """
        response = self.client.post(
            reverse("blog-detail", kwargs={"slug": "blog-1"}), {}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
