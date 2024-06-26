# Generated by Django 4.2.5 on 2023-10-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_alter_movie_options_category_slug_movie_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=255, unique=True, verbose_name="URL"),
        ),
        migrations.AlterField(
            model_name="movie",
            name="slug",
            field=models.SlugField(max_length=255, unique=True, verbose_name="URL"),
        ),
    ]
