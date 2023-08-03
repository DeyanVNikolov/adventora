from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib import messages


def sign_up(request):
    # if user is already logged in, redirect to home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            # check if user exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Потребител с този имейл вече съществува.')
                return redirect('sign-up')

            if len(password) < 8:
                messages.error(request, 'Паролата трябва да съдържа поне 8 символа.')
                return redirect('sign-up')

            if password != password2:
                messages.error(request, 'Паролите не съвпадат.')
                return redirect('sign-up')

            if len(username) < 4:
                messages.error(request, 'Потребителското име трябва да съдържа поне 4 символа.')
                return redirect('sign-up')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Потребител с това потребителско име вече съществува.')
                return redirect('sign-up')

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            messages.success(request, 'Успешна регистрация.')
            return redirect('home')


    else:
        form = RegisterForm()
    return render(request, 'auth/sign_up.html', {'form': form})


def sign_in(request):
    # if user is already logged in, redirect to home page
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm()
    return render(request, 'auth/sign_in.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    return redirect('home')
