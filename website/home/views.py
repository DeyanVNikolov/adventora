import datetime
import os
import uuid
from pathlib import Path

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SecurityCheckForm
from hotel.models import Hotel, Room, Reservation

from django.utils.translation import gettext as _

from hotel.models import Luxury


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
                response.set_cookie('report-to', value=f'https://report.adventora.net/security-token/access/{request.user.id}/v/n/{unix_now}', max_age=3600, httponly=False, samesite='Strict', secure=True, path='/')
                return response
        return render(request, 'security_check.html', {'form': form})


def emergency_in_bg(request):
    return render(request, 'emergency_in_bg.html')


def stranded_abroad(request):
    return render(request, 'stranded_abroad.html')


def hotels(request):
    hotels = Hotel.objects.all().exclude(approved=False)

    for hotel in hotels:
        # select ONE random image from hotel.photos
        photos = str(hotel.photos).split('|PHOTO|')
        if len(photos) > 0:
            img = None
            for photo in photos:
                host = request.get_host()
                scheme = request.scheme
                
                r = requests.get(f'{scheme}://{host}/static/cover/hotel/{hotel.id}/{photo}')
                if r.status_code == 200:
                    img = photo
                    break
            if img:
                print("SELECTED IMAGE: " + img)
                hotel.main_img = img
            else:
                print("NO IMAGE FOUND")
                hotel.main_img = None

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
        people = request.POST.get('people', 1)
        checkin = request.POST.get('checkin', None)
        checkout = request.POST.get('checkout', None)

        if not checkin or not checkout:
            messages.error(request, _('Invalid dates'))
            return redirect('room', room_id=room_id)

        checkin = datetime.datetime.strptime(checkin, '%Y-%m-%d')
        checkout = datetime.datetime.strptime(checkout, '%Y-%m-%d')
        nights = (checkout - checkin).days

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


# handle /static/invoices route
@login_required
def invoicesserve(request, reservation_id):

    try:
        uuid.UUID(reservation_id)
    except ValueError:
        messages.error(request, _('Reservation not available'))
        return redirect('home')

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        messages.error(request, _('Reservation not available'))
        return redirect('home')

    if not reservation:
        messages.error(request, _('Reservation not available'))
        return redirect('home')

    if reservation.reserved_by != request.user.id:
        messages.error(request, _('Reservation not available'))
        return redirect('home')

    BASE_DIR = Path(__file__).resolve().parent.parent
    filename = f'{BASE_DIR}/invoices/reservation-{reservation.id}.html'

    if not os.path.isfile(filename):
        messages.error(request, _('Invoice not available'))
        return redirect('hotels')


    # display the invoice, using utf-8 encoding

    return HttpResponse(open(filename, encoding='utf-8').read(), content_type='text/html; charset=utf-8', status=200, reason='OK - ACCESS GRANTED', charset='utf-8')



def invoice(request, reservation_id):
    try:
        uuid.UUID(reservation_id)
    except ValueError:
        messages.error(request, _('Reservation not available'))
        return redirect('hotels')

    reservation = Reservation.objects.get(id=reservation_id)
    if not reservation:
        messages.error(request, _('Reservation not available'))
        return redirect('hotels')

    if reservation.reserved_by != request.user.id:
        messages.error(request, _('Reservation not available'))
        return redirect('hotels')

    context = {
        'reservation': reservation
    }

    return render(request, 'invoice.html', context)


def handle404(request, exception):
    return render(request, '404.html', status=404)


def handle500(request):
    # ADD HEADER ERR-REF: <uuid>

    response = render(request, '500.html', status=500)
    response['ERR-REF'] = str(uuid.uuid4())
    response['ERR-REF-URL'] = str(request.build_absolute_uri())
    response['ERR-REF-USER'] = str(request.user.id) if request.user.is_authenticated else 'anonymous'
    response['ERR-EXPLAIN'] = 'Internal Server Error, Adventora encountered an unexpected error while processing your request. Please try again later. Contact it@adventora.net if the problem persists.'
    response['ERR-GOBACK'] = 'https://adventora.net'
    response['ERR-CONTACT'] = 'https://adventora.net/contact; it@adventora.net'
    response['ERR-RETRY'] = 'https://adventora.net'
    response['ERR-RETRY-TEXT'] = 'Retry'
    response['ERR-GOBACK-TEXT'] = 'Go Back'
    response['RETRY-AFTER'] = '3600'


    return response