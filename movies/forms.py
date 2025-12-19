from django import forms
from .models import Movie
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
