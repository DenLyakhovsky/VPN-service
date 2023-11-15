from django.contrib import admin
from .models import UserProfile

# happy: 12345qwe


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'last_name')


admin.site.register(UserProfile, UserProfileAdmin)
