from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Страница приложения cinema_app.")


def categories(request):
    return HttpResponse("<h1>Фильмы по категориям</h1>")