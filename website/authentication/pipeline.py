from django.shortcuts import redirect
from .email import sendregisterationemail

def enable_two_factor(backend, user, response, *args, **kwargs):
    if user:
        if user.two_fa_enabled and user.factor is not None and user.factor != '':
            if user.factor_passed:
                user.factor_passed = False
                user.save()
                return redirect("/authentication/two-factor")


def send_welcome_email(backend, user, response, *args, **kwargs):
    if user:
        if user.email is not None and user.email != '' and user.email != ' ' and user.email != 'None' and user.email is not None:
            if user.welcome_email_sent is False or user.welcome_email_sent is None:
                user.welcome_email_sent = True
                user.save()
                name = user.first_name + " " + user.last_name
                sendregisterationemail(user.email, name)