from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .managers import CustomUserManager


def user_avatar_directory_path(instance: "User", filename: str) -> str:
    return f"users/user_{instance.id}/avatar/{filename}"


class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to="users_photos")
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
