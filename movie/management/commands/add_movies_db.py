from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command (BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'
    
    def handle(self, *args, **kwargs):

        json_file_path = 'movie/management/commands/movies.json'
 
        
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
     
        
        for i in range(len(movies)):
            movie = movies[i]
            exist = Movie.objects.filter(title = movie ['title']). first() 
            if True:
                Movie.objects.create(title = movie['title'],
                                    image = 'movie/imagenes/default.jpg',
                                    genre = movie['genre'],
                                    year = movie['year'])

