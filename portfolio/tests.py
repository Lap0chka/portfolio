from django.test import TestCase, Client
from django.urls import reverse
from portfolio.models import Portfolio

class BaseViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio1 = Portfolio.objects.create(
            title="Project 1", description="Description 1", url="http://example.com/1"
        )
        self.portfolio2 = Portfolio.objects.create(
            title="Project 2", description="Description 2", url="http://example.com/2"
        )

    def test_base_view_status_code(self):
        response = self.client.get(reverse('base_view'))
        self.assertEqual(response.status_code, 200)

    def test_base_view_uses_correct_template(self):
        response = self.client.get(reverse('base_view'))
        self.assertTemplateUsed(response, 'portfolio/base.html')

    def test_base_view_context_contains_portfolios(self):
        response = self.client.get(reverse('base_view'))
        self.assertIn('portfolios', response.context)
        self.assertEqual(list(response.context['portfolios']), [self.portfolio1, self.portfolio2])

    def test_base_view_displays_portfolio_titles(self):
        response = self.client.get(reverse('base_view'))
        self.assertContains(response, "Project 1")
        self.assertContains(response, "Project 2")
