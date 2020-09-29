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