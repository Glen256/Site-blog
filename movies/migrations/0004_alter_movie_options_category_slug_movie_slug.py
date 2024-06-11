# Generated by Django 4.2.5 on 2023-10-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_alter_category_options_alter_movie_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="movie",
            options={
                "ordering": ["time_create", "title"],
                "verbose_name": "Кращі кінофільми",
                "verbose_name_plural": "Кращі кінофільми",
            },
        ),
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=255, null=True, verbose_name="URL"),
        ),
        migrations.AddField(
            model_name="movie",
            name="slug",
            field=models.SlugField(max_length=255, null=True, verbose_name="URL"),
        ),
    ]