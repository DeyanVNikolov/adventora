from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Потребителско име или имейл", required=True)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, label="Парола", required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Вход', css_class='is-primary'))
    helper.form_method = 'POST'


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, label="Потребителско име", required=True,
                               help_text="Потребителското име трябва да съдържа поне 8 символа.")
    first_name = forms.CharField(max_length=65, label="Име", required=True)
    last_name = forms.CharField(max_length=65, label="Фамилия", required=True)
    email = forms.EmailField(max_length=65, label="Имейл", help_text="Имейлът трябва да е валиден.", required=True)
    password1 = forms.CharField(max_length=65, label="Парола", widget=forms.PasswordInput,
                                help_text="Паролата трябва да съдържа поне 8 символа. <br> Паролата не трябва да съдържа само цифри. <br> "
                                          "Паролата не трябва да съдържа само букви. <br> Паролата не трябва да съдържа само специални символи. <br> "
                                          "Паролата не трябва да съдържа името на потребителя. <br> Паролата не трябва да съдържа често срещани пароли.",
                                required=True)
    password2 = forms.CharField(max_length=65, label="Повтори паролата", widget=forms.PasswordInput, required=True,
                                help_text="Въведете същата парола, както по-горе, за да потвърдите.")

    class Meta:
        model = User
        fields = ('username', "first_name", "last_name", "email", "password1", "password2")

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Регистрация', css_class='button is-link'))
    helper.form_method = 'POST'


class RoleChoiceForm(forms.Form):
    ROLE_CHOICES = (('user', 'Vacationer - Explore, plan, and book your ideal vacation activities.'), (
        'hotel_manager', 'Hotel Manager - Oversee operations and provide excellent service in your own hotel.'), (
                        'employee',
                        'Employee - Contribute your expertise to a thriving workplace, such as a hotel or guest house.'))

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label='Choose a Role')

    helper = FormHelper()
    helper.form_method = 'post'
    helper.layout = Layout('role', Submit('submit', 'Submit', css_class='btn-primary'))


class CompleteNameForm(forms.Form):
    first_name = forms.CharField(max_length=65, label="Име", required=True)
    last_name = forms.CharField(max_length=65, label="Фамилия", required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Запази', css_class='button is-link'))
    helper.form_method = 'POST'


class CompleteEmailForm(forms.Form):
    email = forms.EmailField(max_length=65, label="Имейл", help_text="Имейлът трябва да е валиден.", required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Запази', css_class='button is-link'))
    helper.form_method = 'POST'


class CompleteUserNameForm(forms.Form):
    username = forms.CharField(max_length=65, label="Потребителско име", required=True,
                               help_text="Потребителското име трябва да съдържа поне 8 символа.")

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Запази', css_class='button is-link'))
    helper.form_method = 'POST'


class EditProfileForm(forms.Form):
    ROLE_CHOICES = (('user', 'Vacationer - Explore, plan, and book your ideal vacation activities.'), (
        'hotel_manager', 'Hotel Manager - Oversee operations and provide excellent service in your own hotel.'), (
                        'employee',
                        'Employee - Contribute your expertise to a thriving workplace, such as a hotel or guest house.'))


    first_name = forms.CharField(max_length=65, label="Име", required=True)
    last_name = forms.CharField(max_length=65, label="Фамилия", required=True)
    email = forms.EmailField(max_length=65, label="Имейл", help_text="Имейлът трябва да е валиден.", required=True)
    username = forms.CharField(max_length=65, label="Потребителско име", required=True,
                                 help_text="Потребителското име трябва да съдържа поне 8 символа.")
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label='Choose a Role')



    helper = FormHelper()
    helper.add_input(Submit('submit', 'Запази', css_class='button is-link'))
    helper.form_method = 'POST'


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=65, label="Стара парола", widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(max_length=65, label="Нова парола", widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(max_length=65, label="Повтори новата парола", widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Запази', css_class='button is-link'))
    helper.form_method = 'POST'


class SetPasswordFromSocialLogin(forms.Form):
    new_password1 = forms.CharField(max_length=65, label="Нова парола", widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(max_length=65, label="Повтори новата парола", widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Запази', css_class='button is-link'))
    helper.form_method = 'POST'


class DeleteAccountForm(forms.Form):
    password = forms.CharField(max_length=65, label="Парола", widget=forms.PasswordInput, required=True)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Изтрий акаунта', css_class='button is-link'))
    helper.form_method = 'POST'

