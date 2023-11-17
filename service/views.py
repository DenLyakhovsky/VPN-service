from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView, FormView
from .forms import *
from .models import UserURL, Click
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import requests
from django.shortcuts import get_object_or_404
from urllib.parse import urljoin


class Home(TemplateView):
    template_name = 'service/home.html'


class AboutSite(TemplateView):
    template_name = 'service/about.html'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_name = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']

            user.username = user_name
            user.last_name = last_name
            user.save()

            login(request, user)
            messages.success(request, 'Successful registration')
            return redirect('home')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegisterForm()
    return render(request, 'service/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'service/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


# View of personal profile
@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'service/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    # We receive data for statistics and links
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = UserURL.objects.filter(user=self.request.user)
        context['clicks'] = Click.objects.filter(user=self.request.user)
        return context


# Updating user data
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'service/user_update.html'
    context_object_name = 'user_update'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Дані оновленні')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_change_form'] = PasswordChangeForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            password_change_form.save()
            messages.success(request, 'Пароль успішно змінений')
            return redirect('profile')
        else:
            messages.error(request, 'Помилка зміни паролю')
            return render(request, 'service/profile.html',
                          {'form': self.get_form(), 'password_change_form': password_change_form})

    def get_success_url(self):
        return reverse_lazy('profile')


# Creation of the URL by the client
@method_decorator(login_required, name='dispatch')
class UserCreateURLView(FormView):
    form_class = UserCreateURLSForm
    template_name = 'service/create_url.html'
    context_object_name = 'create_url_view'

    def form_valid(self, form):
        d = form.cleaned_data
        data = UserURL(user=self.request.user, site_url=d.get('site_url'), site_name=d.get('site_name'))
        data.save()
        return redirect('profile')


# Provy view
@method_decorator(login_required, name='dispatch')
class ProxyView(View):
    def get(self, request, site_url, path):
        user_url = get_object_or_404(UserURL, user=request.user, site_url=site_url)
        base_url = user_url.site_url

        proxied_url = urljoin(base_url, path)

        proxied_url_with_scheme = f'http://localhost:8000/{proxied_url}'

        user_id = request.user.id

        try:
            click = Click.objects.get(user_id=user_id, url=base_url)
        except Click.DoesNotExist:
            click = Click.objects.create(user_id=user_id, url=base_url)

        click.increment_clicks()

        response = requests.get(proxied_url_with_scheme, headers=request.headers)

        return HttpResponse(response.content, content_type=response.headers['content-type'])
