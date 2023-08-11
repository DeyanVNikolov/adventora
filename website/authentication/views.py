from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm, RoleChoiceForm, CompleteNameForm, CompleteEmailForm, CompleteUserNameForm, EditProfileForm, ChangePasswordForm, SetPasswordFromSocialLogin, DeleteAccountForm, CitizenshipForm, PhoneForm, TwoFactorEnableForm, TwoFactorEnableConfirmForm, TwoFactorForm, TwoFactorDisableForm
from django.contrib import messages
from twilio.rest import Client
import os
import pyqrcode
from dotenv import load_dotenv


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

            user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name,
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
                user = CustomUser.objects.filter(email=username).first()
                if user is None:
                    messages.error(request, 'Потребител с този имейл не съществува.')
                    return redirect('sign-in')
                username = user.username

                user = authenticate(request, username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    if request.user.two_fa_enabled is True:
                        request.user.factor_passed = False
                        request.user.save()
                    messages.success(request, 'Успешно влизане.')
                    return redirect('home')
                else:
                    messages.error(request, 'Грешна парола.')
                    return redirect('sign-in')
            else:
                user = CustomUser.objects.filter(username=username).first()
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
            if existing_user is not None and existing_user != request.user:
                messages.error(request, 'Потребител с това потребителско име вече съществува.')
                return redirect('complete-username')

            if username.strip() == '' or username is None or len(username) < 5:
                messages.error(request, 'Невалидно потребителско име. Поне 5 символа.')
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


@login_required
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
            if username.strip() == "" or username is None or len(username) < 5:
                messages.error(request, 'Невалидно потребителско име. Поне 5 символа.')
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
    context = {'form': form, 'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username,
               citizenship: 'citizenship'}
    return render(request, 'auth/edit_profile.html', context)


@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def banned(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    context = {'full_name': full_name}
    return render(request, 'auth/banned.html', context)



load_dotenv(".env")

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")


def generate_qr_code(uri, uuid):
    qr = pyqrcode.create(uri)
    # save qr code as png to settings.STATIC_ROOT
    qr.png(f"static/qr/{uuid}.png", scale=6)


def generate_new_factor(user, uuid):
    client = Client(account_sid, auth_token)

    name = user.first_name + " " + user.last_name

    new_factor = client.verify.v2.services("VAa66c2fc670269be421064b095e18f682").entities(uuid).new_factors.create(
        friendly_name=f"{name}", factor_type='totp')
    generate_qr_code(new_factor.binding['uri'], uuid)

    return new_factor


def verifyfactor(user, id, uuid, code):
    client = Client(account_sid, auth_token)

    factor = user.factor

    id1 = id
    uuid1 = uuid
    code1 = str(code)
    factor1 = factor

    print("--------------------")
    print(id1)
    print(uuid1)
    print(code1)
    print(factor1)
    print("--------------------")

    verifiedfactor = client.verify.v2.services('VAa66c2fc670269be421064b095e18f682').entities(f'{uuid1}').factors(
        f'{factor1}').update(auth_payload=f'{code1}')

    return verifiedfactor


def verifyuser(user, id, uuid, code):
    client = Client(account_sid, auth_token)

    factor = user.factor

    challenge = client.verify.v2.services('VAa66c2fc670269be421064b095e18f682').entities(f'{uuid}').challenges.create(
        auth_payload=f'{code}', factor_sid=f'{factor}')

    return challenge


def resend_verification_email(request):
    return HttpResponse("Not implemented yet.")

@login_required
def two_factor(request):
    if request.user.two_fa_enabled is False:
        messages.error(request, 'Трябва да активирате двуфакторен аутентификатор.')
        return redirect('home')

    if request.user.factor_passed is True:
        messages.error(request, 'Вече сте въвели кода.')
        return redirect('home')

    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            verification = verifyuser(request.user, request.user.id, request.user.uniqueid, code)

            if verification.status == 'approved':
                request.user.factor_passed = True
                request.user.save()
                messages.success(request, 'Успешно въведен код.')
                return redirect('home')
            else:
                messages.error(request, 'Грешен код.')
                return redirect('two-factor')



    form = TwoFactorForm()
    context = {'form': form}
    return render(request, 'auth/two_factor.html', context)


def two_factor_enable(request):
    if request.user.two_fa_enabled is True:
        messages.error(request, 'Вече сте активирали двуфакторен аутентификатор.')
        return redirect('home')
    if request.method == 'POST':
        form = TwoFactorEnableForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not request.user.check_password(password):
                messages.error(request, 'Грешна парола.')
                return redirect('two-factor-enable')

            uuid = request.user.uniqueid

            new_factor = generate_new_factor(request.user, uuid)

            request.user.factor = new_factor.sid
            request.user.save()


            messages.success(request, 'Успешно активиран двуфакторен аутентификатор.')
            return redirect('two-factor-verify')


    form = TwoFactorEnableForm()
    return render(request, 'auth/two_factor_enable.html', {'form': form})


def two_factor_enable_confirm(request):
    if request.user.two_fa_enabled is True:
        messages.error(request, 'Вече сте активирали двуфакторен аутентификатор.')
        return redirect('home')
    if request.method == 'POST':
        form = TwoFactorEnableConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')

            uuid = request.user.uniqueid
            id = request.user.id

            verifiedfactor = verifyfactor(request.user, id, uuid, code)

            if verifiedfactor.status == "verified":
                request.user.two_fa_enabled = True
                request.user.save()
                messages.success(request, 'Успешно активиран двуфакторен аутентификатор.')
                return redirect('home')
            else:
                messages.error(request, 'Грешен код.')
                return redirect('two-factor-verify')



    form = TwoFactorEnableConfirmForm()
    return render(request, 'auth/two_factor_enable_confirm.html', {'form': form})


def two_factor_disable(request):
    if request.user.two_fa_enabled is False:
        messages.error(request, 'Вече сте деактивирали двуфакторен аутентификатор.')
        return redirect('home')

    if request.method == 'POST':
        form = TwoFactorDisableForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not request.user.check_password(password):
                messages.error(request, 'Грешна парола.')
                return redirect('two-factor-disable')

            request.user.two_fa_enabled = False
            request.user.factor = None
            request.user.factor_passed = False
            request.user.save()
            messages.success(request, 'Успешно деактивиран двуфакторен аутентификатор.')
            return redirect('home')

    form = TwoFactorDisableForm()
    return render(request, 'auth/two_factor_disable.html', {'form': form})
