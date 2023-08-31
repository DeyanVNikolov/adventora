from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# import CustomUser model
from .models import Hotel
from .forms import RegisterHotelForm, ConfirmAddressForm
from django.utils.translation import gettext as _

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
        hotel = Hotel.objects.filter(owner=request.user.id).first()
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
        hotel = Hotel.objects.filter(owner=request.user.id).first()
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
    hotel = Hotel.objects.filter(owner=request.user.id).first()
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

            messages.success(request, _('Successfully registered hotel'))
            return redirect('dashboard')
        else:
            print(form.errors.as_data())
            messages.error(request, _('Error while registering hotel'))
            context['form'] = form

            return render(request, 'hotel/register_hotel.html', context)

    hotel = Hotel.objects.filter(owner=request.user.id).first()
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

    hotel = Hotel.objects.filter(owner=request.user.id).first()
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
def rooms(request, hotel_id):
    # TODO Room preview, all rooms
    pass


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
def add_room(request, hotel_id):
    # TODO Room adding
    pass


@login_required
@is_current_user_role_manager
@is_address_confirmed
@is_hotel_confirmed
def room(request, hotel_id, room_id):
    # TODO Room editing, deleting, etc.
    # TODO Room images
    # TODO Room reservations
    pass


