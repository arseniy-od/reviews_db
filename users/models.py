from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

from .managers import EmailUserManager


class MyTitlesUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
        ('django_admin', 'Django Administrator')
    ]
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = EmailUserManager()

    def __str__(self):
        return self.email
