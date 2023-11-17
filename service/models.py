from django.contrib.auth.models import User
from django.db import models


class UserURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_url = models.CharField(max_length=150, verbose_name='Посилання')
    site_name = models.CharField(max_length=150, verbose_name='Назва сайту')

    def __str__(self):
        return f'{self.user} : {self.site_name}'
