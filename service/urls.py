from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
]
