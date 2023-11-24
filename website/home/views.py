import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SecurityCheckForm


def home(request):
    return render(request, 'home.html', {'name': 'Deyan'})


def contacts(request):
    return render(request, 'contact.html')


def partnerships(request):
    return render(request, 'partnerships.html')


def privacy(request):
    return render(request, 'privacy.html')


def security_check(request):
    has_clearance_cookie = request.COOKIES.get('clearance', None)

    url = request.GET.get('url', None)
    if has_clearance_cookie:
        return redirect(url)
    else:
        form = SecurityCheckForm()
        if request.method == 'POST':
            form = SecurityCheckForm(request.POST)
            if form.is_valid():
                unix_now = int(datetime.datetime.now().timestamp())
                unix_plus_ten = unix_now + 3600
                response = redirect(url)
                response.set_cookie('clearance', f'SECURITY_CLEARANCE_COOKIE-DO-NOT-EDIT-OR-DELETE--{request.user.id}--SECURITY_PASSED--DO-NOT-SHARE-COOKIES-{unix_now}-_-{unix_plus_ten}', max_age=3600, httponly=True, samesite='Strict', secure=True, path='/')
                return response
        return render(request, 'security_check.html', {'form': form})


def emergency_in_bg(request):
    return render(request, 'emergency_in_bg.html')