from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ('superuser', 'superuser')
)


class YamdbUser(AbstractUser):
    role = models.CharField('Роль',
                            max_length=16,
                            default='user',
                            choices=CHOICES)
    bio = models.TextField('Биография',
                           blank=True)

    REQUIRED_FIELDS = ['role', 'email']
