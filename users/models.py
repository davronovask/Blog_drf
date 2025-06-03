from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)  # Можешь удалить, если не нужен

    def __str__(self):
        return self.username
