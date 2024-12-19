from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from logger.logger import Logger
from portfolio.models import Portfolio

# Initialize the logger
logger_instance = Logger(__name__)
logger = logger_instance.get_logger()


def base_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the base portfolio view with all portfolio items.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered portfolio/base.html template with portfolio items.
    """
    try:
        portfolios = Portfolio.objects.all()
    except Exception as e:
        portfolios = []
        logger.error(f'Error retrieving portfolios: {e}')

    return render(request, 'portfolio/base.html', {'portfolios': portfolios})
