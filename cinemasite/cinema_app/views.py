from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AddFilmsForm
from .models import Cinema, FeedBack
from .utils import DataMixin


class CinemaHome(DataMixin, ListView):
    template_name = 'cinema_app/index.html'
    context_object_name = 'films'
    title_page = 'Главная страница',
    cat_selected = 0

    def get_queryset(self):
        return Cinema.active.all().select_related('cat')


def about(request):
    context = {
        'title': 'О сайте',
        'cat_selected': 0,
    }
    return render(request, 'cinema_app/about.html', context=context)


class ShowFilm(DataMixin, DetailView):
    template_name = 'cinema_app/film.html'
    slug_url_kwarg = 'film_slug'
    context_object_name = 'film'

    def get_object(self, queryset=None):
        return get_object_or_404(Cinema.active, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = context['film']
        if self.request.user.is_authenticated:
            feedback_exist = FeedBack.objects.filter(author=self.request.user, cinema=film).exists()
            context['feedback_exist'] = feedback_exist
        return self.get_mixin_context(context, title=context['film'].title)


class AddFilm(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddFilmsForm
    template_name = 'cinema_app/add_films.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление фильма'
    login_url = 'users:login'


class AddFeedBack(LoginRequiredMixin, DataMixin, CreateView):
    model = FeedBack
    fields = ['comment']
    template_name = 'cinema_app/addfeedback.html'
    title_page = 'Добавить комментарий'
    login_url = 'users:login'

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.author = self.request.user
        feedback.cinema = Cinema.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        film_slug = self.object.cinema.slug
        return reverse('film', kwargs={'film_slug': film_slug})


class UpdateFilm(LoginRequiredMixin, DataMixin, UpdateView):
    model = Cinema
    fields = '__all__'
    template_name = 'cinema_app/add_films.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование'
    login_url = 'users:login'


class UpdateFeedBack(LoginRequiredMixin, DataMixin, UpdateView):
    model = FeedBack
    fields = ['comment']
    template_name = 'cinema_app/addfeedback.html'
    title_page = 'Изменить комментарий'

    def get_success_url(self):
        film_slug = self.object.cinema.slug
        return reverse('film', kwargs={'film_slug': film_slug})


def contact(request):
    return HttpResponse('Обратная связь')


class CinemaCategory(DataMixin, ListView):
    template_name = 'cinema_app/index.html'
    context_object_name = 'films'
    allow_empty = False

    def get_queryset(self):
        return Cinema.active.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['films'][0].cat
        return self.get_mixin_context(context, title=f'Категория - {cat.name}', cat_selected=cat.pk)


class CinemaGenre(DataMixin, ListView):
    template_name = 'cinema_app/index.html'
    context_object_name = 'films'
    allow_empty = False

    def get_queryset(self):
        return Cinema.active.filter(genres__slug=self.kwargs['genre_slug']).prefetch_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = context['films'][0].genres
        return self.get_mixin_context(context, title=f'Категория - {genre.name}')


class Search(DataMixin, ListView):
    template_name = 'cinema_app/index.html'
    title_page = 'Результат поиска'
    context_object_name = 'films'

    def get_queryset(self):
        return Cinema.active.filter(title__icontains=self.request.GET.get('res'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['res'] = self.request.GET.get('res')
        return self.get_mixin_context(context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена")
