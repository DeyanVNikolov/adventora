from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, label="Потребителско име", required=True, help_text="Потребителското име трябва да съдържа поне 8 символа.")
    first_name = forms.CharField(max_length=65, label="Име", required=True)
    last_name = forms.CharField(max_length=65, label="Фамилия", required=True)
    email = forms.EmailField(max_length=65, label="Имейл", help_text="Имейлът трябва да е валиден.", required=True)
    password1 = forms.CharField(max_length=65, label="Парола", widget=forms.PasswordInput,
                                help_text="Паролата трябва да съдържа поне 8 символа. <br> Паролата не трябва да съдържа само цифри. <br> "
                                          "Паролата не трябва да съдържа само букви. <br> Паролата не трябва да съдържа само специални символи. <br> "
                                          "Паролата не трябва да съдържа името на потребителя. <br> Паролата не трябва да съдържа често срещани пароли.", required=True)
    password2 = forms.CharField(max_length=65, label="Повтори паролата", widget=forms.PasswordInput, required=True, help_text="Въведете същата парола, както по-горе, за да потвърдите.")


    class Meta:
        model = User
        fields = ('username',"first_name", "last_name", "email", "password1", "password2")

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Регистрация', css_class='button is-link'))
    helper.form_method = 'POST'
