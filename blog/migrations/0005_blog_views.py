# Generated by Django 4.2.3 on 2023-12-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_blog_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]