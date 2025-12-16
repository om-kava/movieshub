from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie
from django.db.models import Q
from .forms import MovieForm
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def movie_list(request):
    query = request.GET.get('q')

    movies = Movie.objects.filter(user=request.user)

    if query:
        movies = movies.filter(title__icontains=query)

    movies = movies.order_by('-created_at')

    return render(request, 'movie_list.html', {
        'movies': movies,
        'query': query
    })



@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            messages.success(request, "Movie added successfully.")
            return redirect('movie_list')

    else:
        form = MovieForm()

    return render(request, 'add_movie.html', {'form': form})

@login_required
def update_movie(request, id):
    movie = Movie.objects.get(id=id)
    if movie.user != request.user:
        return redirect('movie_list')

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie updated successfully.")
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'update_movie.html', {'form': form})


@login_required
def delete_movie(request, id):
    movie = Movie.objects.get(id=id)
    if movie.user != request.user:
        return redirect('movie_list')

    movie.delete()
    messages.success(request, "Movie deleted successfully.")
    return redirect('movie_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def movies_api(request):
    movies = Movie.objects.all()

    data = []

    for movie in movies:
        data.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'release_date': movie.release_date.strftime('%Y-%m-%d'),
            'created_at': movie.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'added_by': movie.user.username
        })

    return JsonResponse(data, safe=False)

