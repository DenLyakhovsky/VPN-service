from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('home', Home.as_view(), name='home'),
    path('about', AboutSite.as_view(), name='about'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('profile', UserProfileView.as_view(), name='profile'),
    path('update-user/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('create/', UserCreateURLView.as_view(), name='create'),

    path('<str:site_url>/<path:path>', ProxyView.as_view(), name='proxy_detail_view'),
]
