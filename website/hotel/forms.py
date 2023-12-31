from ckeditor.widgets import CKEditorWidget
from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from turnstile.fields import TurnstileField
from django.contrib.gis import forms as gis_forms
from django.contrib.admin import widgets

from .models import Room


class RegisterHotelForm(forms.Form):
    name = forms.CharField(max_length=100, label=_('Hotel Name'))
    address = gis_forms.PointField(widget=gis_forms.OSMWidget(attrs={'map_height': 600, 'default_zoom': 7.5, 'default_lon': '25.8652148', 'default_lat': '42.5183673'}), label=_('Address'))
    city = forms.CharField(max_length=50, label=_('City'))
    phone = forms.CharField(label=_("Phone"), required=True, widget=forms.TextInput(attrs={'placeholder': '+359 888 888 888'}))
    email = forms.EmailField(max_length=254, label=_('Email'))
    website = forms.CharField(max_length=100, label=_('Website'))
    description = forms.CharField(widget=CKEditorWidget(), label=_('Description'))
    EIK = forms.CharField(max_length=50, label=_('EIK'))
    mol_name = forms.CharField(max_length=100, label=_('Authorized Person'))
    stars = forms.IntegerField(label=_('Stars'), min_value=1, max_value=6)
    read_privacy_policy = forms.BooleanField(
        label=mark_safe(_('I have read and agree to the <a href="/privacy" target="_blank">privacy policy</a>')),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    read_terms_and_conditions = forms.BooleanField(
        label=mark_safe(_('I have read and agree to the <a href="/terms-of-use" target="_blank">terms and conditions</a>')),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    liability = forms.BooleanField(
        label=mark_safe(
            _('I hereby certify, under penalty of law, that the information provided about myself and my hotel is accurate and complete to the best of my knowledge.<br> I understand that any false or misleading information provided may result in the immdiate suspesion of my hotel listing from Adventora and may lead to potential legal consequences.')
        ),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    # captcha = TurnstileField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', _('Register Hotel'),
                            onclick="event.preventDefault(); var form = event.target.form; form.dispatchEvent(new Event('submit', { bubbles: true })); setTimeout(function() { event.target.disabled = true; }, 10);"
                            )
                     )


class ConfirmAddressForm(forms.Form):
    address = forms.CharField(max_length=1000, label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))

    captcha = TurnstileField()
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', _('Confirm Address'),
                            onclick="event.preventDefault(); var form = event.target.form; form.dispatchEvent(new Event('submit', { bubbles: true })); setTimeout(function() { event.target.disabled = true; }, 10);"
                            )
                     )


class EditHotelInfoForm(forms.Form):
    name = forms.CharField(max_length=100, label=_('Hotel Name'))
    address = forms.CharField(max_length=5000, label=_('Address'))
    city = forms.CharField(max_length=50, label=_('City'))
    phone = forms.CharField(label=_("Phone"), required=True, widget=forms.TextInput(attrs={'placeholder': '+359 888 888 888'}))
    email = forms.EmailField(max_length=254, label=_('Email'))
    website = forms.CharField(max_length=100, label=_('Website'))
    description = forms.CharField(widget=CKEditorWidget(), label=_('Description'))
    EIK = forms.CharField(max_length=50, label=_('EIK'))
    mol_name = forms.CharField(max_length=100, label=_('Authorized Person'))
    stars = forms.IntegerField(label=_('Stars'), min_value=1, max_value=6)

    helper = FormHelper()
    helper.form_method = 'POST'
    # disable the button then submit the form to prevent double form submission
    helper.add_input(Submit('submit', _('Save Changes'),
                            onclick="event.preventDefault(); var form = event.target.form; form.dispatchEvent(new Event('submit', { bubbles: true })); setTimeout(function() { event.target.disabled = true; }, 10);"
                            )
                     )


class CreateRoom(forms.Form):
    description = forms.CharField(widget=CKEditorWidget(), label=_('Description'))
    number = forms.IntegerField(label=_('Room Number'))
    price = forms.DecimalField(max_digits=11, decimal_places=2, label=_('Price / Night'))
    capacity = forms.IntegerField(label=_('Capacity'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', _('Create Room'),
                            onclick="event.preventDefault(); var form = event.target.form; form.dispatchEvent(new Event('submit', { bubbles: true })); setTimeout(function() { event.target.disabled = true; }, 10);"
                            )
                     )


class CreateReservationFormHotel(forms.Form):
    # make room number to be a dropdown with all available rooms, from room model.py
    room_choies = Room.objects.all()
    room = forms.ModelChoiceField(queryset=room_choies, label=_('Room'), empty_label=_('Select Room'))

    check_in = forms.DateField(label=_('Check In'), widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(label=_('Check Out'), widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.IntegerField(label=_('Guests'))
    name = forms.CharField(max_length=100, label=_('Name'))
    email = forms.EmailField(max_length=254, label=_('Email'))
    phone = forms.CharField(label=_("Phone"), required=True, widget=forms.TextInput(attrs={'placeholder': '+359 888 888 888'}))
    idcardnumber = forms.CharField(max_length=50, label=_('ID Card Number'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', _('Create Reservation'),
                            onclick="event.preventDefault(); var form = event.target.form; form.dispatchEvent(new Event('submit', { bubbles: true })); setTimeout(function() { event.target.disabled = true; }, 10);"
                            )
                     )