import json
import os
import dotenv
dotenv_file = os.path.join(BASE_DIR, ".env")
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import requests


def eik(request, bulstat=None):
    if bulstat is not None:
        url = os.environ.get('EIK_URL')
        url += bulstat

        response = requests.get(url)
        if response.status_code == 200:
            return HttpResponse(response.content)
        else:
            return HttpResponse('No such EIK')
    else:
        return HttpResponse('No EIK provided')
