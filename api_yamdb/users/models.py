from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('US', 'user'),
    ('MO', 'moderator'),
    ('AD', 'admin'),
    ('SU', 'superuser')
)


class YamdbUser(AbstractUser):
    role = models.CharField('Роль',
                            max_length=16,
                            default='user',
                            choices=CHOICES)
    bio = models.TextField('Биография',
                           blank=True)

    REQUIRED_FIELDS = ['role', 'email']
# class YamdbUser(AbstractUser):
#     username = models.CharField('Имя пользователя',
#                                 max_length=32,
#                                 unique=True)
#     role = models.CharField('Роль',
#                             max_length=16,
#                             default='user',
#                             choices=CHOICES)
#     bio = models.TextField('Биография',
#                            blank=True)
#     email = models.EmailField('Электронная почта',
#                               max_length=254,
#                               unique=True)

#     REQUIRED_FIELDS = ['role', 'email']
