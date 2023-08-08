from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    print("user:", request.user)
    return render(request, 'home.html', {'name': 'Deyan'})


def contacts(request):
    return render(request, 'contact.html')


def partnerships(request):
    return render(request, 'partnerships.html')