# Steps of Create Django REST Framework & Docker with  Permissions & Postgresql

-----(To start a project)------#

## in the terminal

- 1 - Prepare your environment for the project :

    - mkdir 'some folder name'
    - cd 'some folder name '
    - poetry init -n
    - poetry add django djangorestframework
    - poetry add --dev black
    - poetry shell
    - django-admin startproject 'project_name_project' .  (don't forget the dot)
    - python manage.py startapp 'app_name'
    - python manage.py createsuperuser
    - python manage.py migrate
    - python manage.py runserver

---

## in VS Code

- 2 - project.settings :

        # name_project/settings.py
        INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',                        # NEW
        'rubik_cube.apps.RubikCubeConfig',       # NEW
        ]

        ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','localhost']
        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
         }
        }

        REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASS': [
            'rest_framework.permissions.IsAuthenticated',
         ]
        }

---

- 3 - app.model :

        # name_app/models.py
        from django.db import models
        from django.contrib.auth import get_user_model

        class Movie(models.Model):
            title = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
            writers = models.CharField(max_length=64)
            stars = models.CharField(max_length=64)
            poster = models.ImageField()
            genre = models.CharField(max_length=64)

            def __str__(self):
                return self.title

---

- python manage.py makemigrations "name"

- python manage.py migrate

- 4 - project.urls:

        # name_project/urls.py

        from django.contrib import admin
        from django.urls import path,include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api/v1/',include('movies.urls')),
            path('api-auth', include('rest_framework.urls')), # add droplist content Log out & if log out the login will show up
        ]

---

- 5 - app.admin:

        # name_app/admin.py

        from django.contrib import admin

        from .models import Movie

        admin.site.register(Movie)

- 6 - app.urls:

        # name_app/urls.py

        from django.urls import path
        from .views import MovieList , MovieDetails

        urlpatterns = [
            path('movie',MovieList.as_view(), name='movie_list'),
            path('movie/<int:pk>',MovieDetails.as_view(), name='movie_details'),
        ]

---

- 7 - create app/serializer.py to convert data to json:

                from rest_framework import serializers
                from .models import Movie

                class MovieSerializer(serializers.ModelSerializer):
                    class Meta:
                        fields = ('title','writers','stars','poster','genre')
                        model = Movie

---

- 8 - app.views:

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

---

- python manage.py runserver

- in root create Dockerfile inside it write:

            FROM python:3
            ENV PYTHONDONTWRITEBYTECODE 1
            ENV PYTHONUNBUFFERED 1
            RUN mkdir /code
            WORKDIR /code
            COPY requirements.txt /code/
            RUN pip install -r requirements.txt
            COPY . /code/

---

- in root create docker-compose.yml inside it write:

            version: '3'

            services:
            web:
                build: .
                command: python manage.py runserver 0.0.0.0:8000
                volumes:
                - .:/code
                ports:
                - "8000:8000"

                depends_on:
                - db
            db:
                image: postgres:11
                environment:
                    - "POSTGRES_HOST_AUTH_METHOD=trust"

---

- poetry export -f requirements.txt -o requirements.txt

- open docker

- docker-compose up

- open docker-->dashboard --->start--->open in window settings#ALLOWED_HOSTS = ['0.0.0.0','localhost','127.0.0.1']

- or try:
    - docker-compose down
    - docker-compose build
    - docker-compose up

- poetry add psycopg2
- poetry export -f requirements.txt -o requirements.txt
- exit poetry
- docker-compose run web python manage.py makemirgation
- docker-compose run web ptyhon manage.py migrate
- docker-compose run web python manage.py createsuperuser
- docker-compose up
to run test :
- docker-compose run web python manage.py test