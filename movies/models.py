from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Текст статті')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Час створення')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Час змінення')
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категорія')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Найкращі статті'
        verbose_name_plural = 'Найкращі статі'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категорія")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id']

class Comments(models.Model):
    user = models.ForeignKey(User,
                             verbose_name="Користувач",
                             on_delete=models.CASCADE)
    new = models.ForeignKey(Movie,
                            verbose_name='пост',
                            on_delete=models.CASCADE)
    text = models.TextField("Коментарій")
    created = models.DateTimeField("Дата добавлення: ", auto_now_add=True, null=True)
    moderation = models.BooleanField("Модерація", default=False)

    class Meta:
        verbose_name = "Коментарій"
        verbose_name_plural = "Коментарій"

    def __str__(self):
        return "{}".format(self.user)