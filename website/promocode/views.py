from django.http import HttpResponse
from django.shortcuts import render


def check(request):
    return HttpResponse("Hello, world. You're at the polls index.")
