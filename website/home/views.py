import datetime
import os
import uuid
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SecurityCheckForm
from hotel.models import Hotel, Room, Reservation

from django.utils.translation import gettext as _


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
                response.set_cookie('clearance', f'SECURITY_CLEARANCE_COOKIE-DO-NOT-EDIT-OR-DELETE--{request.user.id}--SECURITY_PASSED--DO-NOT-SHARE-COOKIES-{unix_now}-_-{unix_plus_ten}',
                                    max_age=3600, httponly=True, samesite='Strict', secure=True, path='/'
                                    )
                return response
        return render(request, 'security_check.html', {'form': form})


def emergency_in_bg(request):
    return render(request, 'emergency_in_bg.html')


def stranded_abroad(request):
    return render(request, 'stranded_abroad.html')


def hotels(request):
    hotels = Hotel.objects.all()

    context = {
        'hotels': hotels
    }
    return render(request, 'hotels.html', context)


def hotel(request, hotel_id):
    try:
        uuid.UUID(hotel_id)
    except ValueError:
        messages.error(request, 'Hotel not available')
        return redirect('hotels')

    hotel = Hotel.objects.get(id=hotel_id)
    if not hotel:
        messages.error(request, 'Hotel not available')
        return redirect('hotels')

    hotel_images = []
    BASE_DIR = Path(__file__).resolve().parent.parent

    image_dir = f'{BASE_DIR}/static/cover/hotel/{hotel.id}'
    if os.path.isdir(image_dir):
        for filename in os.listdir(image_dir):
            hotel_images.append(filename)

    rooms = Room.objects.filter(hotel=hotel)

    context = {
        'hotel': hotel,
        'hotel_images': hotel_images,
        'rooms': rooms
    }
    return render(request, 'hotel.html', context)


@login_required
def room(request, room_id):
    try:
        uuid.UUID(room_id)
    except ValueError:
        messages.error(request, _('Room not available'))
        return redirect('hotels')

    room = Room.objects.get(id=room_id)
    if not room:
        messages.error(request, _('Room not available'))
        return redirect('hotels')

    hotel = room.hotel

    if request.method == 'POST':
        name = request.user.first_name + " " + request.user.last_name
        email = request.user.email
        nights = request.POST.get('nights', 1)
        people = request.POST.get('people', 1)
        checkin = request.POST.get('checkin', None)
        checkout = request.POST.get('checkout', None)

        if not checkin or not checkout:
            messages.error(request, _('Invalid dates'))
            return redirect('room', room_id=room_id)

        checkin = datetime.datetime.strptime(checkin, '%Y-%m-%d')
        checkout = datetime.datetime.strptime(checkout, '%Y-%m-%d')
        price = room.price * int(nights)

        reservation = Reservation()

        reservation.hotel = hotel
        reservation.room = room
        reservation.reserved_by = request.user.id
        reservation.checkin = checkin
        reservation.checkout = checkout
        reservation.price = price
        reservation.status = 'pending'
        reservation.people = people

        reservation.save()

        from .email import sendreservationsuccess
        sendreservationsuccess(email, name, checkin, checkout, people, nights, price, reservation, hotel, room)

        messages.success(request, _('Reservation successful'))
        return redirect('hotels')


    context = {
        'room': room,
        'hotel': hotel
    }

    return render(request, 'room.html', context)


def handle404(request, exception):
    return render(request, '404.html', status=404)