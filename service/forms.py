from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserURL


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Імʼя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    last_name = forms.CharField(label='Прізвище', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторення пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'last_name', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Імʼя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'last_name']


class UserCreateURLSForm(forms.ModelForm):
    class Meta:
        model = UserURL
        fields = ['site_url', 'site_name']

