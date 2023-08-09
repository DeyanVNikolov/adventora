from captcha.fields import CaptchaField
from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.gis.geos import Point
from django_countries.fields import CountryField, LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from location_field.forms.plain import PlainLocationField
from location_field.forms.spatial import LocationField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


# name = models.CharField(max_length=100)
# address = models.CharField(max_length=100)
# city = models.CharField(max_length=50)
# country = models.CharField(max_length=50)
# phone = models.CharField(max_length=50)
# email = models.EmailField(max_length=254)
# website = models.CharField(max_length=100)
# description = models.TextField()
# EIK = models.CharField(max_length=50)
# owner = models.CharField(max_length=100)
# stars = models.IntegerField()


class RegisterHotelForm(forms.Form):
    name = forms.CharField(max_length=100, label='Име на хотела')
    address = PlainLocationField(based_fields=['city'], zoom=6, label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}),initial=Point(25.355996814032515, 42.71891178252764))
    city = forms.CharField(max_length=50, label='Град')
    phone = PhoneNumberField(label='Телефонен номер', widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, label='Имейл')
    website = forms.CharField(max_length=100, label='Уебсайт')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    EIK = forms.CharField(max_length=50, label='ЕИК')
    mol_name = forms.CharField(max_length=100, label='МОЛ')
    stars = forms.IntegerField(label='Звезди', min_value=1, max_value=6)
    captcha = CaptchaField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Регистрирай хотела'))


class ConfirmAddressForm(forms.Form):
    address = forms.CharField(max_length=1000, label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Потвърди адреса'))
