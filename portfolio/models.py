from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Portfolio(TranslatableModel):
    """
    A model representing a portfolio project or work.

    Attributes:
        title (str): The title of the portfolio item.
        translations (str): A detailed description of the portfolio item (translatable).
        tools (str): The tools or technologies used in the project.
        is_it (str): Additional information or a category.
        image (ImageField): An optional image representing the portfolio item.
        link (URLField): An optional URL linking to the portfolio item.
    """

    title: models.CharField = models.CharField(
        max_length=128,
        verbose_name="Title",
        help_text="Enter the title of the portfolio item.",
    )

    translations = TranslatedFields(
        description=models.TextField(
            verbose_name="Description",
            help_text="Enter a detailed description of the portfolio item.",
        )
    )

    tools: models.TextField = models.TextField(
        blank=True,
        null=True,
        verbose_name="Tools",
        help_text="List the tools or technologies used in the project.",
    )

    is_it: models.CharField = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        default="",
        verbose_name="Category",
        help_text="Enter a category or additional information.",
    )

    image = models.ImageField(
        upload_to="portfolio/",
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Upload an image representing the portfolio item.",
    )

    link: models.URLField = models.URLField(
        blank=True,
        null=True,
        verbose_name="Link",
        help_text="Enter a URL linking to the portfolio item.",
    )

    def __str__(self) -> str:
        """
        String representation of the Portfolio model.

        Returns:
            str: The title of the portfolio item.
        """
        return str(self.title)

    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"
        ordering = ["title"]
