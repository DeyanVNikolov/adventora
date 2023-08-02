from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = RegisterForm()
    return render(request, 'auth/sign_up.html', {'form': form})


def login(request):
    form = AuthenticationForm()
    return render(request, 'auth/sign_in.html', {'form': form})
