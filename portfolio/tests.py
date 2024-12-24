from typing import Any

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from portfolio.models import Portfolio


class BaseViewTests(TestCase):
    """
    Tests for the base view of the portfolio app.
    """

    def setUp(self) -> None:
        """
        Set up test data for the portfolio view.
        """
        self.client: Client = Client()

        # Create a test image
        self.test_image: SimpleUploadedFile = SimpleUploadedFile(
            name="test_image.jpg",
            content=(
                b"\x47\x49\x46\x38\x37\x61\x01\x00\x01\x00\x80\x00\x00"
                b"\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x01\x00"
                b"\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b"
            ),
            content_type="image/jpeg",
        )

        # Create portfolio items
        self.portfolio1: Portfolio = Portfolio.objects.create(
            title="Project 1",
            description="Description 1",
            image=self.test_image,
        )
        self.portfolio2: Portfolio = Portfolio.objects.create(
            title="Project 2",
            description="Description 2",
            image=self.test_image,
        )

    def test_base_view_status_code(self) -> None:
        """
        Test that the base view returns a status code of 200.
        """
        response = self.client.get(reverse("portfolio"))
        self.assertEqual(response.status_code, 200)

    def test_base_view_uses_correct_template(self) -> None:
        """
        Test that the base view uses the correct template.
        """
        response = self.client.get(reverse("portfolio"))
        self.assertTemplateUsed(response, "portfolio/index.html")

    def test_base_view_context_contains_portfolios(self) -> None:
        """
        Test that the base view context contains portfolio items.
        """
        response = self.client.get(reverse("portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)
        self.assertIn("portfolios", response.context)
        self.assertQuerySetEqual(
            response.context["portfolios"],
            Portfolio.objects.all(),
            transform=lambda x: x,
        )

    def test_base_view_displays_portfolio_titles(self) -> None:
        """
        Test that the portfolio titles are displayed on the page.
        """
        response: Any = self.client.get(reverse("portfolio"))
        self.assertContains(response, "Project 1")
        self.assertContains(response, "Project 2")
