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
from django.utils.translation import gettext as _

from .models import CustomUser


def security_check(view_func):
    def wrapper(request, *args, **kwargs):
        has_clearance_cookie = request.COOKIES.get('clearance', None)
        if not has_clearance_cookie:
            return redirect(f'/security-check?url={request.path}')
        else:
            if has_clearance_cookie:
                value = request.COOKIES.get('clearance')
                if not value.startswith(f'SECURITY_CLEARANCE_COOKIE-DO-NOT-EDIT-OR-DELETE--{request.user.id}--SECURITY_PASSED--DO-NOT-SHARE-COOKIES'):
                    messages.error(request, _('Malformed security token'))
                    response = redirect(f'/security-check?url={request.path}')
                    response.delete_cookie('clearance')
                    return response

        return view_func(request, *args, **kwargs)

    return wrapper

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
                messages.error(request, _('A user with that email already exists.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            if len(password) < 8:
                messages.error(request, _('Password must be at least 8 characters long.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            if password != password2:
                messages.error(request, _('Passwords do not match.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            if len(username) < 4:
                messages.error(request, _('Username must be at least 4 characters long.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            # no symbols in username
            if not username.isalnum():
                messages.error(request, _('Username should only contain letters and numbers.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            # is email valid, e.g has @, domain, etc.
            if not email.isalnum():
                messages.error(request, _('Invalid email.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            if User.objects.filter(username=username).exists():
                messages.error(request, _('A user with that username already exists.'))
                return render(request, 'auth/sign_up.html', {'form': form})

            user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                                  last_name=last_name
                                                  )
            user.save()
            login(request, user)
            messages.success(request, _('Successfully registration.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            print(form.errors.as_data())
            return render(request, 'auth/sign_up.html', {'form': form})


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
                    messages.error(request, _('A user with that email does not exist.'))
                    return render(request, 'auth/sign_in.html', {'form': form})
                username = user.username

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if request.user.two_fa_enabled is True:
                        request.user.factor_passed = False
                        request.user.save()
                    messages.success(request, _('Successfully logged in.'))
                    return redirect('/')
                else:
                    messages.error(request, _('Invalid password.'))
                    return render(request, 'auth/sign_in.html', {'form': form})
            else:
                user = CustomUser.objects.filter(username=username).first()
                if user is None:
                    messages.error(request, _('A user with that username does not exist.'))
                    return render(request, 'auth/sign_in.html', {'form': form})
                else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, _('Successfully logged in.'))
                        return redirect('/')
                    else:
                        messages.error(request, _('Invalid password.'))
                        return render(request, 'auth/sign_in.html', {'form': form})

        else:
            messages.error(request, _('Invalid data.'))
            print(form.errors.as_data())
            return render(request, 'auth/sign_in.html', {'form': form})
    form = LoginForm()
    return render(request, 'auth/sign_in.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    messages.success(request, _('Successfully logged out.'))
    return redirect('home')


@login_required
def choose_role(request):

    if request.method == 'POST':
        form = RoleChoiceForm(request.POST)
        if form.is_valid():
            role_choices = ["user", "hotel_manager", "employee"]
            role = form.cleaned_data.get('role')
            if role not in role_choices:
                messages.error(request, _('Invalid role.'))
                return render(request, 'auth/choose_role.html', {'form': form})
            request.user.role = role
            request.user.confirmedrole = True
            request.user.save()
            messages.success(request, _('Successfully chosen role.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/choose_role.html', {'form': form})

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
            messages.success(request, _('Successfully confirmed name.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/completeprofile.html', {'form': form})

    form = CompleteNameForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name})
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {'form': form, 'first_name': first_name, 'last_name': last_name}
    return render(request, 'auth/completeprofile.html', context)


@login_required
def complete_email(request):
    if request.method == 'POST':
        form = CompleteEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            existing_user = CustomUser.objects.filter(email=email).first()
            if existing_user is not None:
                if existing_user != request.user:
                    messages.error(request, _('A user with that email already exists.'))
                    return render(request, 'auth/completeprofile.html', {'form': form})

            request.user.email = email
            request.user.confirmedemail = True
            request.user.save()
            messages.success(request, _('Successfully confirmed email.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/completeprofile.html', {'form': form})

    form = CompleteEmailForm(initial={'email': request.user.email})
    email = request.user.email
    context = {'form': form, 'email': email, }
    return render(request, 'auth/completeprofile.html', context)


@login_required
def complete_username(request):
    if request.method == 'POST':
        form = CompleteUserNameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            existing_user = CustomUser.objects.filter(username=username).first()
            if existing_user is not None and existing_user != request.user:
                messages.error(request, _('A user with that username already exists.'))
                return render(request, 'auth/completeprofile.html', {'form': form})

            if username.strip() == '' or username is None or len(username) < 5:
                messages.error(request, _('Invalid username. At least 5 characters.'))
                return render(request, 'auth/completeprofile.html', {'form': form})

            request.user.username = username
            request.user.confirmedusername = True
            request.user.save()
            messages.success(request, _('Successfully confirmed username.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/completeprofile.html', {'form': form})

    form = CompleteUserNameForm(initial={'username': request.user.username})
    username = request.user.username
    context = {'form': form, 'username': username, }
    return render(request, 'auth/completeprofile.html', context)


@login_required
@security_check
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            email = form.cleaned_data.get('email')
            existing_user = CustomUser.objects.filter(email=email).first()
            if existing_user is not None and existing_user != request.user:
                messages.error(request, _('A user with that email already exists.'))
                return render(request, 'auth/edit_profile.html', {'form': form})

            username = form.cleaned_data.get('username')
            existing_user = CustomUser.objects.filter(username=username).first()
            if existing_user is not None and existing_user != request.user:
                messages.error(request, _('A user with that username already exists.'))
                return render(request, 'auth/edit_profile.html', {'form': form})
            if username.strip() == "" or username is None or len(username) < 5:
                messages.error(request, _('Invalid username. At least 5 characters.'))
                return render(request, 'auth/edit_profile.html', {'form': form})

            role_choices = ["user", "hotel_manager", "employee"]
            role = form.cleaned_data.get('role')
            if role not in role_choices:
                messages.error(request, _('Invalid role.'))
                return render(request, 'auth/edit_profile.html', {'form': form})

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
            messages.success(request, _('Successfully edited profile.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/edit_profile.html', {'form': form})

    form = EditProfileForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                    'email': request.user.email, 'username': request.user.username,
                                    'role': request.user.role, 'citizenship': request.user.citizenship,
                                    'phone': request.user.phone}
                           )
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    username = request.user.username
    citizenship = request.user.citizenship
    context = {'form': form, 'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username,
               citizenship: 'citizenship'}
    return render(request, 'auth/edit_profile.html', context)


@login_required
@security_check
def change_password(request):
    if request.method == 'POST':
        if request.user.has_usable_password():
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')

                if not request.user.check_password(old_password):
                    messages.error(request, _('Incorrect old password.'))
                    return redirect('change-password')

                if new_password1 != new_password2:
                    messages.error(request, _('Passwords do not match.'))
                    return redirect('change-password')

                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, _('Successfully changed password.'))
                return redirect('home')
            else:
                messages.error(request, _('Invalid data.'))
                return render(request, 'auth/change_password.html', {'form': form})

        else:
            form = SetPasswordFromSocialLogin(request.POST)
            if form.is_valid():
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')

                if new_password1 != new_password2:
                    messages.error(request, _('Passwords do not match.'))
                    return render(request, 'auth/change_password.html', {'form': form})

                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, _('Successfully changed password.'))
                return redirect('home')
            else:
                messages.error(request, _('Invalid data.'))
                return render(request, 'auth/change_password.html', {'form': form})
    if request.user.has_usable_password():
        form = ChangePasswordForm()
    else:
        form = SetPasswordFromSocialLogin()
    return render(request, 'auth/change_password.html', {'form': form})


@login_required
@security_check
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not request.user.check_password(password):
                messages.error(request, _('Incorrect password.'))
                return redirect('delete-account')

            request.user.delete()
            messages.success(request, _('Successfully deleted account.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/delete_account.html', {'form': form})

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
            messages.success(request, _('Successfully confirmed citizenship.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/completeprofile.html', {'form': form})

    form = CitizenshipForm(initial={'citizenship': request.user.citizenship})
    citizenship = request.user.citizenship
    context = {'form': form, 'citizenship': citizenship, }
    return render(request, 'auth/completeprofile.html', context)


@login_required
def complete_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')

            request.user.phone = phone
            request.user.confirmedphone = True
            request.user.save()
            messages.success(request, _('Successfully confirmed phone number.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/completeprofile.html', {'form': form})

    form = PhoneForm(initial={'phone': request.user.phone})
    phone = request.user.phone
    context = {'form': form, 'phone': phone, }
    return render(request, 'auth/completeprofile.html', context)


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
        friendly_name=f"{name}", factor_type='totp'
    )
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
        f'{factor1}'
    ).update(auth_payload=f'{code1}')

    return verifiedfactor


def verifyuser(user, id, uuid, code):
    client = Client(account_sid, auth_token)

    factor = user.factor

    challenge = client.verify.v2.services('VAa66c2fc670269be421064b095e18f682').entities(f'{uuid}').challenges.create(
        auth_payload=f'{code}', factor_sid=f'{factor}'
    )

    return challenge


def resend_verification_email(request):
    return HttpResponse("Not implemented yet.")


@login_required
def two_factor(request):
    if request.user.two_fa_enabled is False:
        messages.error(request, _('Two factor authentication is not enabled.'))
        return redirect('home')

    if request.user.factor_passed is True:
        messages.error(request, _('Two factor authentication is already passed.'))
        return redirect('home')

    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            verification = verifyuser(request.user, request.user.id, request.user.id, code)

            if verification.status == 'approved':
                request.user.factor_passed = True
                request.user.save()
                messages.success(request, _('Successfully passed two factor authentication'))
                return redirect('home')
            else:
                messages.error(request, _('Invalid code.'))
                return redirect('two-factor')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/two_factor.html', {'form': form})

    form = TwoFactorForm()
    context = {'form': form}
    return render(request, 'auth/two_factor.html', context)


@login_required
@security_check
def two_factor_enable(request):
    if request.user.two_fa_enabled is True:
        messages.error(request, _('Two factor authentication is already enabled.'))
        return redirect('home')

    if request.user.password.startswith('!'):
        messages.error(request, _('You cannot enable two factor authentication with a social login.'))
        return redirect('edit-profile')


    if request.method == 'POST':
        form = TwoFactorEnableForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not request.user.check_password(password):
                messages.error(request, _('Incorrect password.'))
                return redirect('two-factor-enable')

            uuid = request.user.id

            new_factor = generate_new_factor(request.user, uuid)

            request.user.factor = new_factor.sid
            request.user.save()

            messages.success(request, _('Successfully enabled two factor authentication.'))
            return redirect('two-factor-verify')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/two_factor_enable.html', {'form': form})

    form = TwoFactorEnableForm()
    return render(request, 'auth/two_factor_enable.html', {'form': form})

@login_required
@security_check
def two_factor_enable_confirm(request):
    if request.user.two_fa_enabled is True:
        messages.error(request, _('Two factor authentication is already enabled.'))
        return redirect('home')
    if request.method == 'POST':
        form = TwoFactorEnableConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            uuid = request.user.id
            id = request.user.id

            verifiedfactor = verifyfactor(request.user, id, uuid, code)

            if verifiedfactor.status == "verified":
                request.user.two_fa_enabled = True
                request.user.factor_passed = True
                request.user.save()
                # delete qr code
                file = f"static/qr/{uuid}.png"
                if os.path.exists(file):
                    os.remove(file)
                messages.success(request, _('Successfully enabled two factor authentication.'))
                return redirect('home')
            else:
                messages.error(request, _('Invalid code.'))
                return redirect('two-factor-verify')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/two_factor_enable_confirm.html', {'form': form})

    form = TwoFactorEnableConfirmForm()
    return render(request, 'auth/two_factor_enable_confirm.html', {'form': form})


@login_required
@security_check
def two_factor_disable(request):
    if request.user.two_fa_enabled is False:
        messages.error(request, _('Two factor authentication is not enabled.'))
        return redirect('home')

    if request.method == 'POST':
        form = TwoFactorDisableForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not request.user.check_password(password):
                messages.error(request, _('Incorrect password.'))
                return redirect('two-factor-disable')

            request.user.two_fa_enabled = False
            request.user.factor = None
            request.user.factor_passed = False
            request.user.save()
            messages.success(request, _('Successfully disabled two factor authentication.'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid data.'))
            return render(request, 'auth/two_factor_disable.html', {'form': form})

    form = TwoFactorDisableForm()
    return render(request, 'auth/two_factor_disable.html', {'form': form})


def login_error(request):
    return render(request, 'auth/login_error.html')