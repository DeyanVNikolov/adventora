import os
import uuid

from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# import CustomUser model
from .models import Hotel, Room
from .forms import RegisterHotelForm, ConfirmAddressForm, CreateRoom, EditHotelInfoForm
from django.utils.translation import gettext as _
from django.contrib.gis.geos import Point
from django.contrib.gis import gdal

from authentication.models import CustomUser


def security_check(view_func):
    def wrapper(request, *args, **kwargs):
        has_clearance_cookie = request.COOKIES.get('clearance', None)
        if not has_clearance_cookie:
            return redirect(f'/security-check?url={request.path}')
        else:
            if has_clearance_cookie:
                value = request.COOKIES.get('clearance')
                if not value.startswith(f'SECURITY_CLEARANCE_COOKIE-DO-NOT-EDIT-OR-DELETE--{request.user.id}--SECURITY_PASSED--DO-NOT-SHARE-COOKIES'):
                    messages.error(request, _('Malformed security token'))
                    response = redirect(f'/security-check?url={request.path}')
                    response.delete_cookie('clearance')
                    return response

        return view_func(request, *args, **kwargs)

    return wrapper


def is_address_confirmed(func):
    def wrapper(request, *args, **kwargs):
        hotel = request.user.hotel
        if hotel and hotel.address_confirmed is False:
            return redirect('confirm-address')
        return func(request, *args, **kwargs)

    return wrapper


def is_current_user_role_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'hotel_manager':
            messages.warning(request, _('You do not have permission to view this page'))
            return redirect('/')
        return func(request, *args, **kwargs)

    return wrapper


def is_hotel_confirmed(func):
    def wrapper(request, *args, **kwargs):
        hotel = request.user.hotel
        if hotel and hotel.approved is False:
            messages.warning(request, _('Your hotel is not approved yet'))
            return redirect('dashboard')
        return func(request, *args, **kwargs)

    return wrapper


def mainpage(request):
    return redirect('dashboard')


@login_required
@is_current_user_role_manager
@is_address_confirmed
@security_check
def dashboard(request):
    context = {}
    hotel = request.user.hotel
    if hotel:
        rooms = hotel.rooms.all()
        context['rooms'] = rooms

    context['hotel'] = hotel

    return render(request, 'hotel/dashboard.html', context)


@login_required
@is_current_user_role_manager
@security_check
def register_hotel(request):
    context = {}

    if request.method == 'POST':
        form = RegisterHotelForm(request.POST)
        if form.is_valid():
            from opencage.geocoder import OpenCageGeocode
            from pyproj import Transformer
            hotel = Hotel()
            hotel.name = form.cleaned_data['name']
            point = form.cleaned_data['address']
            latitude = point.y
            longitude = point.x

            transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
            latitude, longitude = transformer.transform(longitude, latitude)

            geocoder = OpenCageGeocode(f'{os.getenv("OPENCAGE_API_KEY")}')
            result = geocoder.reverse_geocode(latitude, longitude)
            hotel.address = f"{latitude},{longitude}"
            if result and result[0]['formatted']:
                hotel.address_text = result[0]['formatted']
            else:
                hotel.address_text = "Address not found"

            hotel.city = form.cleaned_data['city']
            hotel.country = "BG"
            hotel.phone = form.cleaned_data['phone']
            hotel.email = form.cleaned_data['email']
            hotel.website = form.cleaned_data['website']
            hotel.description = form.cleaned_data['description']
            hotel.EIK = form.cleaned_data['EIK']
            hotel.mol_name = form.cleaned_data['mol_name']
            hotel.owner = request.user
            hotel.stars = form.cleaned_data['stars']
            hotel.save()

            request.user.hotel = hotel
            request.user.save()

            messages.success(request, _('Successfully registered hotel'))
            return redirect('dashboard')
        else:
            print(form.errors.as_data())
            messages.error(request, _('Error while registering hotel'))
            context['form'] = form

            return render(request, 'hotel/register_hotel.html', context)

    hotel = request.user.hotel
    if hotel:
        messages.warning(request, _('You have already registered a hotel'))
        return redirect('dashboard')

    form = RegisterHotelForm()

    context['form'] = form

    return render(request, 'hotel/register_hotel.html', context)


@login_required
@is_current_user_role_manager
@security_check
def confirm_address(request):
    context = {}

    hotel = request.user.hotel
    if not hotel:
        messages.warning(request, _('You have not registered a hotel yet'))
        return redirect('register-hotel')

    context['hotel'] = hotel

    latlon = hotel.address.split(",")
    lat = latlon[0]
    lon = latlon[1]

    context['lat'] = lat
    context['lon'] = lon

    if request.method == 'POST':
        form = ConfirmAddressForm(request.POST)
        if form.is_valid():
            hotel.address_text = form.cleaned_data['address']
            hotel.address_confirmed = True
            hotel.save()
            messages.success(request, _('Successfully confirmed address'))
            return redirect('dashboard')
        else:
            messages.error(request, _('Error while confirming address'))
            return render(request, 'hotel/confirm_address.html', {'form': form})

    form = ConfirmAddressForm(initial={'address': hotel.address_text})
    context['form'] = form

    return render(request, 'hotel/confirm_address.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
@security_check
def hotel(request, hotel_id):
    data = Hotel.objects.filter(uid=hotel_id).first()
    if not data:
        messages.warning(request, _('No such hotel'))
        return redirect('dashboard')

    if data.owner.id != request.user.id:
        messages.warning(request, _('You do not have permission to view this page'))
        return redirect('dashboard')

    context = {'hotel': data}

    return render(request, 'hotel/hotel.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
def add_room(request, hotel_id):

    try:
        uuid.UUID(hotel_id)
    except ValueError:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    hotel = Hotel.objects.filter(id=hotel_id).first()

    if not hotel:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    if request.user.hotel != hotel:
        messages.warning(request, _('You do not have permission to view this page'))
        return redirect('dashboard')

    if request.method == 'POST':
        form = CreateRoom(request.POST)
        if form.is_valid():
            room = Room()
            room.hotel = hotel
            room.description = form.cleaned_data['description']
            room.number = form.cleaned_data['number']
            room.capacity = form.cleaned_data['capacity']
            room.price = form.cleaned_data['price']
            room.status = "Available"

            room.save()
            messages.success(request, _('Successfully added room'))
            return redirect('dashboard')
        else:
            messages.error(request, _('Error while adding room'))
            return render(request, 'hotel/add_room.html', {'hotel': hotel, 'form': form})

    context = {
        'hotel': hotel,
        'form': CreateRoom()
    }

    return render(request, 'hotel/add_room.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
@security_check
def room(request, hotel_id, room_id):
    try:
        uuid.UUID(hotel_id)
    except ValueError:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    hotel = Hotel.objects.filter(id=hotel_id).first()
    if not hotel:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    if request.user.hotel != hotel:
        messages.warning(request, _('You do not have permission to view this page'))
        return redirect('dashboard')

    # check if valid UUID
    try:
        uuid.UUID(room_id)
    except ValueError:
        messages.warning(request, _('We cannot find the room you are looking for'))
        return redirect('dashboard')

    room = hotel.rooms.filter(id=room_id).first()

    if not room:
        messages.warning(request, _('We cannot find the room you are looking for'))
        return redirect('dashboard')

    context = {
        'hotel': hotel,
        'room': room
    }

    return render(request, 'hotel/room.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
@security_check
def edit_hotel(request):
    hotel = request.user.hotel
    if not hotel:
        messages.warning(request, _('You have not registered a hotel yet'))
        return redirect('register-hotel')

    if request.method == 'POST':
        form = EditHotelInfoForm(request.POST)
        if form.is_valid():
            hotel.name = form.cleaned_data['name']
            hotel.address_text = form.cleaned_data['address']

            hotel.city = form.cleaned_data['city']
            hotel.country = "BG"
            hotel.phone = form.cleaned_data['phone']
            hotel.email = form.cleaned_data['email']
            hotel.website = form.cleaned_data['website']
            hotel.description = form.cleaned_data['description']
            hotel.EIK = form.cleaned_data['EIK']
            hotel.mol_name = form.cleaned_data['mol_name']
            hotel.owner = request.user
            hotel.stars = form.cleaned_data['stars']
            hotel.save()

            messages.success(request, _('Successfully updated hotel'))
            return redirect('dashboard')
        else:
            print(form.errors.as_data())
            messages.error(request, _('Error while updating hotel'))
            context = {'form': form}

            return render(request, 'hotel/edit_hotel.html', context)

    form = EditHotelInfoForm(initial={
        'name': hotel.name,
        'address': hotel.address_text,
        'city': hotel.city,
        'phone': hotel.phone,
        'email': hotel.email,
        'website': hotel.website,
        'description': hotel.description,
        'EIK': hotel.EIK,
        'mol_name': hotel.mol_name,
        'stars': hotel.stars,
    }
    )

    context = {'form': form}

    return render(request, 'hotel/edit_hotel.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
def updateroomstatus(request, hotel_id, room_id, status):
    try:
        uuid.UUID(hotel_id)
    except ValueError:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')


    hotel = Hotel .objects.filter(id=hotel_id).first()
    if not hotel:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    if request.user.hotel != hotel:
        messages.warning(request, _('You do not have permission to view this page'))
        return redirect('dashboard')

    try:
        uuid.UUID(room_id)
    except ValueError:
        messages.warning(request, _('We cannot find the room you are looking for'))
        return redirect('dashboard')

    room = hotel.rooms.filter(id=room_id).first()

    if not room:
        messages.warning(request, _('We cannot find the room you are looking for'))
        return redirect('dashboard')

    if status == 'ava':
        room.status = 'Available'
        room.save()
        messages.success(request, _('Successfully updated room status'))
        return redirect('room', hotel_id=hotel_id, room_id=room_id)

    elif status == 'occ':
        room.status = 'Occupied'
        room.save()
        messages.success(request, _('Successfully updated room status'))
        return redirect('room', hotel_id=hotel_id, room_id=room_id)

    elif status == 'tbc':
        room.status = 'ForCleaning'
        room.save()
        messages.success(request, _('Successfully updated room status'))
        return redirect('room', hotel_id=hotel_id, room_id=room_id)

    else:
        messages.warning(request, _('Invalid status'))
        return redirect('room', hotel_id=hotel_id, room_id=room_id)


def occupy(request, hotel_id, room_id):
    try:
        uuid.UUID(hotel_id)
    except ValueError:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    hotel = Hotel.objects.filter(id=hotel_id).first()
    if not hotel:
        messages.warning(request, _('We cannot find the hotel you are looking for'))
        return redirect('dashboard')

    if request.user.hotel != hotel:
        messages.warning(request, _('You do not have permission to view this page'))
        return redirect('dashboard')

    try:
        uuid.UUID(room_id)
    except ValueError:
        messages.warning(request, _('We cannot find the room you are looking for'))
        return redirect('dashboard')

    room = hotel.rooms.filter(id=room_id).first()
    if not room:
        messages.warning(request, _('We cannot find the room you are looking for'))
        return redirect('dashboard')

    if room.occupied:
        messages.warning(request, _('This room is already occupied'))
        return redirect('room', hotel_id=hotel_id, room_id=room_id)

    context = {
        'hotel': hotel,
        'room': room
    }
    return render(request, 'hotel/occupy.html', context=context)
