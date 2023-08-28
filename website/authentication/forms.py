
from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django_countries.fields import CountryField, LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from turnstile.fields import TurnstileField

from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label=_("Username or email"), required=True)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, label=_("Password"), required=True)
    captcha = TurnstileField()

    class Meta:
        model = User
        fields = ('username', 'password')

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Login'), css_class='is-primary'))
    helper.form_method = 'POST'


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, label=_("Username"), required=True,
                               help_text=_("The username must contain at least 8 characters.")
                               )
    first_name = forms.CharField(max_length=65, label=_("First name"), required=True)
    last_name = forms.CharField(max_length=65, label=_("Last name"), required=True)
    email = forms.EmailField(max_length=65, label=_("Email"), help_text=_("Email address must be valid"), required=True)
    password1 = forms.CharField(max_length=65, label=_("Password"), widget=forms.PasswordInput,
                                help_text=_("The password must be at least 8 characters long. <br> The password should not contain only digits. <br> "
                                            "The password should not contain only letters. <br> The password should not contain only special characters. <br> "
                                            "The password should not contain the username. <br> The password should not be a commonly used password."
                                            ),
                                required=True
                                )
    password2 = forms.CharField(max_length=65, label=_("Confirm password"), widget=forms.PasswordInput, required=True,
                                help_text=_("Enter the same password as above, for verification.")
                                )
    captcha = TurnstileField()

    class Meta:
        model = User
        fields = ('username', "first_name", "last_name", "email", "password1", "password2")

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Sign up'), css_class='button is-link'))
    helper.form_method = 'POST'


class RoleChoiceForm(forms.Form):
    ROLE_CHOICES = (('user', _('Vacationer - Explore, plan, and book your ideal vacation activities.')),
                     ('hotel_manager', _('Hotel Manager - Oversee operations and provide excellent service in your own hotel.')),
                     ('employee', _('Employee - Contribute your expertise to a thriving workplace, such as a hotel or guest house.')))

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label='Choose a Role')

    helper = FormHelper()
    helper.form_method = 'post'
    helper.layout = Layout('role', Submit('submit', _('Submit'), css_class='btn-primary'))


class CompleteNameForm(forms.Form):
    first_name = forms.CharField(max_length=65, label=_("First Name"), required=True)
    last_name = forms.CharField(max_length=65, label=_("Last Name"), required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'


class CompleteEmailForm(forms.Form):
    email = forms.EmailField(max_length=65, label=_("Email"), help_text=_("The email must be valid."), required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class CompleteUserNameForm(forms.Form):
    username = forms.CharField(max_length=65, label=_("Username"), required=True,
                               help_text=_("The username must contain at least 8 characters.")
                               )

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class EditProfileForm(forms.Form):
    ROLE_CHOICES = (('user', _('Vacationer - Explore, plan, and book your ideal vacation activities.')),
                     ('hotel_manager', _('Hotel Manager - Oversee operations and provide excellent service in your own hotel.')),
                     ('employee', _('Employee - Contribute your expertise to a thriving workplace, such as a hotel or guest house.')))

    first_name = forms.CharField(max_length=65, label=_("First Name"), required=True)
    last_name = forms.CharField(max_length=65, label=_("Last Name"), required=True)
    email = forms.EmailField(max_length=65, label=_("Email"), help_text=_("The email must be valid."), required=True)
    username = forms.CharField(max_length=65, label=_("Username"), required=True,
                               help_text=_("The username must contain at least 8 characters.")
                               )
    citizenship = CountryField(blank_label='(select country)').formfield(label=_("Citizenship"), required=True)
    phone = forms.CharField(label=_("Phone"), required=True, widget=forms.TextInput(attrs={'placeholder': '+359 888 888 888'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label=_('Choose a Role'))

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=65, label=_("Old Password"), widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(max_length=65, label=_("New Password"), widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(max_length=65, label=_("Confirm New Password"), widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class SetPasswordFromSocialLogin(forms.Form):
    new_password1 = forms.CharField(max_length=65, label=_("New Password"), widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(max_length=65, label=_("Confirm New Password"), widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class DeleteAccountForm(forms.Form):
    password = forms.CharField(max_length=65, label=_("Password"), widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Delete Account'), css_class='button is-link'))
    helper.form_method = 'POST'



class CitizenshipForm(forms.Form):

    class Meta:
        model = CustomUser
        fields = ('citizenship',)
        widgets = {'citizenship': CountrySelectWidget()}

    citizenship = CountryField().formfield(label=_("Citizenship"), required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class PhoneForm(forms.Form):
    phone = forms.CharField(label=_("Phone"), required=True, widget=forms.TextInput(attrs={'placeholder': '+359 888 888 888'}))

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Save'), css_class='button is-link'))
    helper.form_method = 'POST'



class TwoFactorEnableForm(forms.Form):
    password = forms.CharField(max_length=65, label=_("Password"), widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Enable'), css_class='button is-link'))
    helper.form_method = 'POST'



class TwoFactorEnableConfirmForm(forms.Form):
    code = forms.CharField(max_length=65, label=_("Code"), required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Enable'), css_class='button is-link'))
    helper.form_method = 'POST'



class TwoFactorForm(forms.Form):
    code = forms.CharField(max_length=65, label=_("Code"), required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Enable'), css_class='button is-link'))
    helper.form_method = 'POST'



class TwoFactorDisableForm(forms.Form):
    password = forms.CharField(max_length=65, label=_("Password"), widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', _('Disable'), css_class='button is-link'))
    helper.form_method = 'POST'

