# Generated by Django 4.2.3 on 2023-12-25 20:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="is_it",
            field=models.CharField(blank=True, default="", max_length=64, null=True),
        ),
    ]
