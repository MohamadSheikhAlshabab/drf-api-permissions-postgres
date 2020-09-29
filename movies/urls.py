from django.urls import path
from .views import MovieList , MovieDetails

urlpatterns = [
    path('movie',MovieList.as_view(), name='movie_list'),
    path('movie/<int:pk>',MovieDetails.as_view(), name='movie_details'),
]