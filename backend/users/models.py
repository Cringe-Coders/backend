from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .managers import CustomUserManager


class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to="users_photos", default="users_photos/no_photo.png")
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, default="")
    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
