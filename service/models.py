from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class UserURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    site_url = models.CharField(max_length=150, verbose_name='Посилання')
    site_name = models.CharField(max_length=150, verbose_name='Назва сайту')

    def __str__(self):
        return f'{self.user} : {self.site_name}'


class Click(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='Користувач')
    url = models.URLField(_("Посилання"), unique=True)
    click_count = models.PositiveIntegerField(_("Кількість кліків"), default=0)

    def increment_clicks(self):
        self.click_count += 1
        self.save()
        return self.click_count

    class Meta:
        verbose_name = _("URL click")
        verbose_name_plural = _("URL clicks")

    def __str__(self):
        return f'{self.user}: {self.url} | {self.click_count}'
