import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from portfolio.models import Portfolio

# Initialize the logger
logger = logging.getLogger(__name__)


def base_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the base portfolio view with all portfolio items.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered portfolio/index.html template with portfolio items.
    """
    try:
        portfolios = Portfolio.objects.all()
    except Exception as e:
        portfolios = []
        logger.error(f"Error retrieving portfolios: {e}")

    return render(request, "portfolio/index.html", {"portfolios": portfolios})
