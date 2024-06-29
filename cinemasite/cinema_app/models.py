from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Cinema.Status.ACTIVE)


class Cinema(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        ACTIVE = 1, 'Активный'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    descriptions = models.TextField(blank=True, verbose_name='Описание фильма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    year_production = models.PositiveIntegerField(blank=True, verbose_name='Год производства')
    is_active = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                    default=Status.ACTIVE, verbose_name='Статус')
    photo = models.ImageField(upload_to='photos_films/', default=None, blank=True, null=True, verbose_name='Фото')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='cinema', verbose_name='Категория')
    genres = models.ManyToManyField('GenreFilm', related_name='cinema_genres', blank=True, verbose_name='Жанры')

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильмы'
        verbose_name_plural = 'Фильмы'
        ordering = ['time_create']
        indexes = [
            models.Index(fields=['time_create']),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(str(self.title)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('film', kwargs={'film_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=250, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(str(self.name)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class GenreFilm(models.Model):
    genre = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=True)

    def __str__(self):
        return self.genre

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(str(self.genre)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})


class FeedBack(models.Model):
    comment = models.TextField(blank=True, verbose_name='Отзыв')
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='feedbackcinema')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='feedbackauthor', null=True)

    def __str__(self):
        return self.comment
