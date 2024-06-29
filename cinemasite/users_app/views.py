from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users_app.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users_app/login.html'
    extra_context = {
        'title': 'Авторизация'
    }

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users_app/register.html'
    extra_context = {'title': 'Регистрация пользователя'}
    success_url = reverse_lazy('users:login')
