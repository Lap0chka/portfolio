from django.contrib import admin
from parler.admin import TranslatableAdmin

from portfolio.models import Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(TranslatableAdmin):
    """
    Admin class for managing Portfolio model with translation support.
    """

    list_display = ("title", "is_it", "link")
    search_fields = ("title", "translations__description")
    list_filter = ("is_it",)
