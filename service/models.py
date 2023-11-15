from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Імʼя')
    last_name = models.CharField(max_length=150, verbose_name='Прізвище')

    def __str__(self):
        return f'Користувач: {self.user}'
