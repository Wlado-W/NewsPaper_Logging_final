from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.sites.models import Site
from datetime import datetime
from django.contrib.auth.models import Group


# from django.core.validators import MinValueValidator


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    # Методы like() и dislike() в моделях Comment и Post увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод preview() модели Post возвращает начало статьи (предварительный просмотр) длиной 124 символа
    # и добавляет многоточие в конце.
    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'title: {self.title} || text: {self.text} || dateCreation: {self.dateCreation}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryThrough}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'text: {self.text} || commentUser: {self.commentUser}'

    # Методы like() и dislike() в моделях Comment и Post увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class CustomSite(Site):
    is_active = models.BooleanField(default=True, verbose_name='Is Active')

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'

class CommonGroup(Group):
    class Meta:
        verbose_name = 'common'
        verbose_name_plural = 'common'

class Appointment(models.Model):
            date = models.DateField(
                default=datetime.utcnow,
            )
            client_name = models.CharField(
                max_length=200
            )
            message = models.TextField()

            def __str__(self):
                return f'{self.client_name}: {self.message}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')