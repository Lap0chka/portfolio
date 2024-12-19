from django.db import models


class Portfolio(models.Model):
    """
    A model representing a portfolio project or work.
    """

    title = models.CharField(
        max_length=128,
        help_text="Title of the portfolio item."
    )

    description = models.TextField(
        help_text="Detailed description of the portfolio item, including tools and techniques used."
    )

    tools = models.TextField(blank=True, null=True)

    is_it = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        default="",
        help_text="A brief categorization or type of the portfolio item."
    )

    image = models.ImageField(
        upload_to='portfolio/media',
        help_text="Upload an image representing the portfolio item.",
        blank=True,
        null=True
    )
    link = models.URLField(
        blank=True,
        null=True,
        help_text="Optional URL linking to more details or the live project."
    )

    def __str__(self) -> str:
        """
        String representation of the Portfolio model.

        Returns:
            str: The title of the portfolio item.
        """
        return str(self.title)
