from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/update/<int:id>/', views.update_movie, name='update_movie'),
    path('movies/delete/<int:id>/', views.delete_movie, name='delete_movie'),
    path('api/movies/', views.movies_api, name='movies_api'),

]
