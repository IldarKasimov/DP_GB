from django import template
from django.db.models import Count

from cinema_app.models import Category, GenreFilm
from cinema_app.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('cinema_app/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('cinema')).filter(total__gt=0)
    context = {
        'cats': cats,
        'cat_selected': cat_selected,
    }
    return context


@register.inclusion_tag('cinema_app/list_genre.html', takes_context=True)
def show_genres(context):
    genres = GenreFilm.objects.annotate(total=Count('cinema_genres')).filter(total__gt=0)
    return {'genres': genres}
