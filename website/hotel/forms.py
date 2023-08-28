
from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.gis.geos import Point
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField, LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from location_field.forms.plain import PlainLocationField
from location_field.forms.spatial import LocationField
from turnstile.fields import TurnstileField

from .models import Room, LuxuryOption
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _


class RegisterHotelForm(forms.Form):
    name = forms.CharField(max_length=100, label=_('Hotel Name'))
    address = PlainLocationField(based_fields=['city'], zoom=6, label=_('Address'), initial=Point(25.355996814032515, 42.71891178252764), widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=50, label=_('City'))
    phone = forms.CharField(label=_("Phone"), required=True, widget=forms.TextInput(attrs={'placeholder': '+359 888 888 888'}))
    email = forms.EmailField(max_length=254, label=_('Email'))
    website = forms.CharField(max_length=100, label=_('Website'))
    description = forms.CharField(widget=CKEditorWidget(), label=_('Description'))
    EIK = forms.CharField(max_length=50, label=_('EIK'))
    mol_name = forms.CharField(max_length=100, label=_('Authorized Person'))
    stars = forms.IntegerField(label=_('Stars'), min_value=1, max_value=6)
    captcha = TurnstileField()
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
            _('I hereby certify, under penalty of law, that the information provided about myself and my hotel is accurate and complete to the best of my knowledge.<br> I understand that any false or misleading information provided may result in the immdiate suspesion of my hotel listing from Adventora and may lead to potential legal consequences.')),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


    helper=FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', _('Register Hotel')))


class ConfirmAddressForm(forms.Form):
    address = forms.CharField(max_length=1000, label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', _('Confirm Address')))

# class Room(models.Model):
#     types_of_luxuries_choices = (
#         ('ac', 'Климатик'), ('tv', 'Телевизор'), ('wifi', 'Wi-Fi'), ('fridge', 'Хладилник'), ('bathroom', 'Баня'),
#         ('balcony', 'Балкон'), ('kitchen', 'Кухня'), ('iron', 'Ютия'), ('hairdryer', 'Сешоар'), ('safe', 'Сейф'),
#         ('phone', 'Телефон'), ('desk', 'Бюро'), ('sofa', 'Диван'), ('fireplace', 'Камина'),
#         ('ventilation', 'Вентилация'),)
#     unique_id = models.CharField(max_length=100, null=True, blank=True, default=str(uuid.uuid4()))
#     hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='hotel_room')
#     name = models.CharField(max_length=100, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     capacity = models.IntegerField(null=True, blank=True)
#     image = models.ImageField(upload_to='room_images', null=True, blank=True)
#     luxuries = MultiSelectField(choices=types_of_luxuries_choices, null=True, blank=True, default='ac', widget=forms.CheckboxSelectMultiple, label='Удобства')


# class RegisterRoomForm(forms.Form):
#     name = forms.CharField(max_length=100, label='Име на стаята')
#     description = forms.CharField(widget=forms.Textarea, label='Описание')
#     price = forms.DecimalField(max_digits=10, decimal_places=2, label='Цена')
#     capacity = forms.IntegerField(label='Капацитет')
#     image = forms.ImageField(label='Снимка', required=False)
#     luxuries = forms.ModelMultipleChoiceField(queryset=LuxuryOption.objects.all(),
#                                               widget=forms.CheckboxSelectMultiple, label='Удобства')
#
#     helper = FormHelper()
#     helper.form_method = 'POST'
#     helper.add_input(Submit('submit', 'Регистрирай стаята'))
