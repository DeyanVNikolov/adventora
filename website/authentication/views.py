from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm, RoleChoiceForm, CompleteNameForm, CompleteEmailForm, CompleteUserNameForm, EditProfileForm, ChangePasswordForm, SetPasswordFromSocialLogin, DeleteAccountForm, CitizenshipForm, PhoneForm
from django.contrib import messages

from .models import CustomUser


def sign_up(request):
    # if user is already logged in, redirect to home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            # check if user exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Потребител с този имейл вече съществува.')
                return redirect('sign-up')

            if len(password) < 8:
                messages.error(request, 'Паролата трябва да съдържа поне 8 символа.')
                return redirect('sign-up')

            if password != password2:
                messages.error(request, 'Паролите не съвпадат.')
                return redirect('sign-up')

            if len(username) < 4:
                messages.error(request, 'Потребителското име трябва да съдържа поне 4 символа.')
                return redirect('sign-up')

            # no symbols in username
            if not username.isalnum():
                messages.error(request, 'Потребителското име трябва да съдържа само букви и цифри.')
                return redirect('sign-up')

            # is email valid, e.g has @, domain, etc.
            if not email.isalnum():
                messages.error(request, 'Невалиден имейл.')
                return redirect('sign-up')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Потребител с това потребителско име вече съществува.')
                return redirect('sign-up')

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            user.save()
            login(request, user)
            messages.success(request, 'Успешна регистрация.')
            return redirect('home')


    else:
        form = RegisterForm()
    return render(request, 'auth/sign_up.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        print("POST")
        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # username is either email or username
            if '@' in username:
                user = User.objects.filter(email=username).first()
                if user is None:
                    messages.error(request, 'Потребител с този имейл не съществува.')
                    return redirect('sign-in')
                username = user.username

                user = authenticate(request, username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Успешно влизане.')
                    return redirect('home')
                else:
                    messages.error(request, 'Грешна парола.')
                    return redirect('sign-in')
            else:
                user = User.objects.filter(username=username).first()
                if user is None:
                    messages.error(request, 'Потребител с това потребителско име не съществува.')
                    return redirect('sign-in')
                else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Успешно влизане.')
                        return redirect('home')
                    else:
                        messages.error(request, 'Грешна парола.')
                        return redirect('sign-in')
    form = LoginForm()
    return render(request, 'auth/sign_in.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    messages.success(request, 'Успешно излизане.')
    return redirect('home')


@login_required
def choose_role(request):

    if request.method == 'POST':
        form = RoleChoiceForm(request.POST)
        if form.is_valid():
            role_choices = ["user", "hotel_manager", "employee"]
            role = form.cleaned_data.get('role')
            if role not in role_choices:
                messages.error(request, 'Невалидна роля.')
                return redirect('choose-role')
            request.user.role = role
            request.user.confirmedrole = True
            request.user.save()
            messages.success(request, 'Успешно избрана роля.')
            return redirect('home')

    form = RoleChoiceForm()
    return render(request, 'auth/choose_role.html', {'form': form})


@login_required
def complete_name(request):
    if request.method == 'POST':
        form = CompleteNameForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.confirmedname = True
            request.user.save()
            messages.success(request, 'Успешно попълнено име.')
            return redirect('home')

    form = CompleteNameForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name})
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {'form': form, 'first_name': first_name, 'last_name': last_name}
    return render(request, 'auth/complete_name.html', context)


@login_required
def complete_email(request):
    if request.method == 'POST':
        form = CompleteEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            existing_user = CustomUser.objects.filter(email=email).first()
            if existing_user is not None:
                if existing_user != request.user:
                    messages.error(request, 'Потребител с този имейл вече съществува.')
                    return redirect('complete-email')

            request.user.email = email
            request.user.confirmedemail = True
            request.user.save()
            messages.success(request, 'Успешно попълнен имейл.')
            return redirect('home')

    form = CompleteEmailForm(initial={'email': request.user.email})
    email = request.user.email
    context = {'form': form, 'email': email, }
    return render(request, 'auth/complete_email.html', context)


@login_required
def complete_username(request):
    if request.method == 'POST':
        form = CompleteUserNameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            existing_user = CustomUser.objects.filter(username=username).first()
            if existing_user is not None:
                if existing_user != request.user:
                    messages.error(request, 'Потребител с това потребителско име вече съществува.')
                    return redirect('complete-username')

            request.user.username = username
            request.user.confirmedusername = True
            request.user.save()
            messages.success(request, 'Успешно попълнено потребителско име.')
            return redirect('home')

    form = CompleteUserNameForm(initial={'username': request.user.username})
    username = request.user.username
    context = {'form': form, 'username': username, }
    return render(request, 'auth/complete_username.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            email = form.cleaned_data.get('email')
            existing_user = CustomUser.objects.filter(email=email).first()
            if existing_user is not None and existing_user != request.user:
                messages.error(request, 'Потребител с този имейл вече съществува.')
                return redirect('edit-profile')

            username = form.cleaned_data.get('username')
            existing_user = CustomUser.objects.filter(username=username).first()
            if existing_user is not None and existing_user != request.user:
                messages.error(request, 'Потребител с това потребителско име вече съществува.')
                return redirect('edit-profile')

            role_choices = ["user", "hotel_manager", "employee"]
            role = form.cleaned_data.get('role')
            if role not in role_choices:
                messages.error(request, 'Невалидна роля.')
                return redirect('edit-profile')

            citizenship = form.cleaned_data.get('citizenship')
            phone = form.cleaned_data.get('phone')

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.username = username
            request.user.role = role
            request.user.citizenship = citizenship
            request.user.phone = phone
            request.user.save()
            messages.success(request, 'Успешно редактиран профил.')
            return redirect('home')

    form = EditProfileForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                    'email': request.user.email, 'username': request.user.username,
                                    'role': request.user.role, 'citizenship': request.user.citizenship,
                                    'phone': request.user.phone})
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    username = request.user.username
    citizenship = request.user.citizenship
    context = {'form': form, 'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username, citizenship: 'citizenship'}
    return render(request, 'auth/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        if request.user.has_usable_password():
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')

                if not request.user.check_password(old_password):
                    messages.error(request, 'Грешна парола.')
                    return redirect('change-password')

                if new_password1 != new_password2:
                    messages.error(request, 'Паролите не съвпадат.')
                    return redirect('change-password')

                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Успешно сменена парола.')
                return redirect('home')

        else:
            form = SetPasswordFromSocialLogin(request.POST)
            if form.is_valid():
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')

                if new_password1 != new_password2:
                    messages.error(request, 'Паролите не съвпадат.')
                    return redirect('change-password')

                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Успешно сменена парола.')
                return redirect('home')
    if request.user.has_usable_password():
        form = ChangePasswordForm()
    else:
        form = SetPasswordFromSocialLogin()
    return render(request, 'auth/change_password.html', {'form': form})


def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not request.user.check_password(password):
                messages.error(request, 'Грешна парола.')
                return redirect('delete-account')

            request.user.delete()
            messages.success(request, 'Успешно изтрит потребител.')
            return redirect('home')

    form = DeleteAccountForm()
    return render(request, 'auth/delete_account.html', {'form': form})


def complete_citizenship(request):
    if request.method == 'POST':
        form = CitizenshipForm(request.POST)
        if form.is_valid():
            citizenship = form.cleaned_data.get('citizenship')

            request.user.citizenship = citizenship
            request.user.confirmedcitizenship = True
            request.user.save()
            messages.success(request, 'Успешно попълнено гражданство.')
            return redirect('home')

    form = CitizenshipForm(initial={'citizenship': request.user.citizenship})
    citizenship = request.user.citizenship
    context = {'form': form, 'citizenship': citizenship, }
    return render(request, 'auth/complete_citizenship.html', context)


def complete_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')

            request.user.phone = phone
            request.user.confirmedphone = True
            request.user.save()
            messages.success(request, 'Успешно попълнен телефонен номер.')
            return redirect('home')

    form = PhoneForm(initial={'phone': request.user.phone})
    phone = request.user.phone
    context = {'form': form, 'phone': phone, }
    return render(request, 'auth/complete_phonenumber.html', context)


def banned(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    context = {'full_name': full_name}
    return render(request, 'auth/banned.html', context)