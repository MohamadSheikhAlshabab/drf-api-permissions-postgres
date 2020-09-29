from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Movies

class MovieTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='testuser', password='password')
        test_user.save()


        test_Movies = Movies.objects.create(
            writers = test_user,
            title = 'The Revenant',
            body = "Leonardo DiCaprio"
        )
        test_Movies.save() 

        

    def test_Movies_content(self):

        movie = Movies.objects.get(id=1)
        actual_writers = str(movie.writers)
        actual_title = str(movie.title)
        actual_stars = str(movie.stars)

        self.assertEqual(actual_writers, 'testuser')
        self.assertEqual(actual_title, 'The Revenant')
        self.assertEqual(actual_stars, "Leonardo DiCaprio")
