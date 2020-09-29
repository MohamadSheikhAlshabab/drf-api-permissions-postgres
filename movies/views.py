from django.shortcuts import render
from rest_framework import generics
from .models import Movie
from .serializer import MovieSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import permissions

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer