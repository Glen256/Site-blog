# Generated by Django 4.2.5 on 2023-11-01 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата добавлення'),
        ),
        migrations.AddField(
            model_name='comments',
            name='moderation',
            field=models.BooleanField(default=False),
        ),
    ]
