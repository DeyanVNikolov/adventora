from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django_countries.fields import CountryField, LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from turnstile.fields import TurnstileField

from django.utils.translation import gettext_lazy as _


class SecurityCheckForm(forms.Form):
    captcha = TurnstileField(attrs={'onchange': 'this.form.submit()'})
