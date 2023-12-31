# Generated by Django 4.2.3 on 2023-07-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Portfolio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("description", models.CharField(max_length=256)),
                ("image", models.ImageField(upload_to="porfolio/midea")),
                ("link", models.URLField(blank=True)),
            ],
        ),
    ]
