from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from softdelete.models import SoftDeleteObject

from .managers import SoftDeleteManagerForSlug
from .mixins import SlugifyMixin

User = get_user_model()


class Title(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='titles')
    genre = models.ManyToManyField('Genre', related_name='titles')
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    rating = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def _get_rating(self):
        reviews = self.reviews.all()
        if reviews:
            rating = 0
            for review in reviews:
                rating += review.score
            rating = rating / reviews.count()
            return rating
        else:
            return None

    def refresh_rating(self):
        self.rating = self._get_rating()
        self.save()


class Category(SlugifyMixin, SoftDeleteObject):
    objects = SoftDeleteManagerForSlug()
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.name


class Genre(SlugifyMixin, SoftDeleteObject):
    objects = SoftDeleteManagerForSlug()
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)


