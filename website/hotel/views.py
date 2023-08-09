from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# import CustomUser model
from .models import Hotel
from website.hotel.forms import RegisterHotelForm, ConfirmAddressForm


def is_address_confirmed(func):
    def wrapper(request, *args, **kwargs):
        hotel = Hotel.objects.filter(owner=request.user.id).first()
        if hotel and hotel.address_confirmed is False:
            return redirect('confirm-address')
        return func(request, *args, **kwargs)
    return wrapper


def is_current_user_role_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'hotel_manager':
            messages.warning(request, 'Нямате права да достъпите тази страница')
            return redirect('/')
        return func(request, *args, **kwargs)
    return wrapper


@login_required
@is_current_user_role_manager
@is_address_confirmed
def home(request):
    return redirect('dashboard')


@login_required
@is_current_user_role_manager
@is_address_confirmed
def dashboard(request):
    context = {}
    hotel = Hotel.objects.filter(owner=request.user.id).first()
    context['hotel'] = hotel

    return render(request, 'hotel/dashboard.html', context)



@login_required
@is_current_user_role_manager
def register_hotel(request):
    context = {}

    if request.method == 'POST':
        form = RegisterHotelForm(request.POST)
        if form.is_valid():
            hotel = Hotel()
            hotel.name = form.cleaned_data['name']
            hotel.address = form.cleaned_data['address']
            latlon = hotel.address.split(",")
            lat = latlon[0]
            lon = latlon[1]
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            response = requests.get(url)
            data = response.json()
            hotel.address_text = data['display_name']

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

            messages.success(request, 'Успешно регистрирахте хотел')
            return redirect('dashboard')
        else:
            print(form.errors.as_data())
            messages.error(request, 'Възникна грешка при регистрацията на хотела')
            context['form'] = form

            return render(request, 'hotel/register_hotel.html', context)

    hotel = Hotel.objects.filter(owner=request.user.id).first()
    if hotel:
        messages.warning(request, 'Вие вече сте регистрирали хотел')
        return redirect('dashboard')

    form = RegisterHotelForm()

    context['form'] = form


    return render(request, 'hotel/register_hotel.html', context)


@login_required
@is_current_user_role_manager
def confirm_address(request):
    context = {}

    hotel = Hotel.objects.filter(owner=request.user.id).first()
    if not hotel:
        messages.warning(request, 'Вие не сте регистрирали хотел')
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
            messages.success(request, 'Успешно потвърдихте адреса')
            return redirect('dashboard')
        else:
            messages.error(request, 'Възникна грешка при потвърждаването на адреса')

    form = ConfirmAddressForm(initial={'address': hotel.address_text})
    context['form'] = form

    return render(request, 'hotel/confirm_address.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
def hotel(request, hotel_id):
    data = Hotel.objects.filter(unique_id=hotel_id).first()
    if not data:
        messages.warning(request, 'Няма такъв хотел')
        return redirect('dashboard')

    if int(data.owner.id) != int(request.user.id):
        messages.warning(request, 'Няма такъв хотел')
        return redirect('dashboard')


    context = {'hotel': data}

    return render(request, 'hotel/hotel.html', context)


@login_required
@is_current_user_role_manager
@is_address_confirmed
def rooms(request, hotel_id):
    # TODO Room preview, all rooms
    pass


@login_required
@is_current_user_role_manager
@is_address_confirmed
def add_room(request, hotel_id):
    # TODO Room adding
    pass


@login_required
@is_current_user_role_manager
@is_address_confirmed
def room(request, hotel_id, room_id):
    # TODO Room editing, deleting, etc.
    # TODO Room images
    # TODO Room reservations
    pass

