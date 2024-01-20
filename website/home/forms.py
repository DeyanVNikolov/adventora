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
    comment = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label="",
        initial="За да продължите, трябва да преминете автоматизирана проверка на сигурността.",
    )
    captcha = TurnstileField(attrs={'onchange': 'this.form.submit()'})


    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        'comment',
        'captcha',

    )
    # disabled
    helper.add_input(Submit('submit', 'Продължи', css_class='is-success disabledbuttonforsecurity', disabled=True,
                            )
                     )

