# models.py trong ứng dụng authentication
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )

