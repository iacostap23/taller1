from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def signuo(request):
    email= request.Get.get('email')
    return render(request, 'signup.html', {'email': email})


def statistics_view(request):
    matplotlib.use('Agg')

    # Gráfica de películas por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year_isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(12, 6)) 
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center', color='blue')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')

    
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=60, ha='right', fontsize=10)

    
    plt.subplots_adjust(bottom=0.4)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Gráfica de películas por género
    genres = Movie.objects.values_list('genre', flat=True)
    movie_counts_by_genre = {}

    for genre in genres:
        if genre:
            first_genre = genre.split(',')[0]  # Tomar solo el primer género
        else:
            first_genre = "Unknown"

        movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    bar_positions_genre = range(len(movie_counts_by_genre))

    plt.figure(figsize=(12, 6))  
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='green')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')

    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=60, ha='right', fontsize=10)


    plt.subplots_adjust(bottom=0.4)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png_genre = buffer.getvalue()
    buffer.close()
    graphic_genres = base64.b64encode(image_png_genre).decode('utf-8')

    # Renderizar ambas gráficas en la plantilla
    return render(request, 'statistics.html', {'graphic_year': graphic, 'graphic_genres': graphic_genres})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

