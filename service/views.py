from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, UpdateView
from .forms import *
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile


class Home(TemplateView):
    template_name = 'service/home.html'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_name = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']

            # Перевірка, чи не існує вже користувача з таким іменем
            if UserProfile.objects.filter(user__username=user_name).exists():
                messages.error(request, 'This username is already taken. Please choose a different one.')
            else:
                # Якщо користувач не існує, створіть його
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
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'service/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'service/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


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
