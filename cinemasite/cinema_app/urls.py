from django.urls import path
from . import views

urlpatterns = [
    path('', views.CinemaHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addfilm/', views.AddFilm.as_view(), name='add_film'),
    path('contact/', views.contact, name='contact'),
    path('film/<slug:film_slug>/', views.ShowFilm.as_view(), name='film'),
    path('category/<slug:cat_slug>/', views.CinemaCategory.as_view(), name='category'),
    path('genre/<slug:genre_slug>/', views.CinemaGenre.as_view(), name='genre'),
    path('update/<slug:slug>/', views.UpdateFilm.as_view(), name='update'),
    path('search/', views.Search.as_view(), name='search'),
    path('updatefeed/<int:pk>/', views.UpdateFeedBack.as_view(), name='updatefeed'),
    path('addfeed/<int:pk>/', views.AddFeedBack.as_view(), name='add_feed'),
]
