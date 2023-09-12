from django.shortcuts import redirect


def enable_two_factor(backend, user, response, *args, **kwargs):
    if user:
        if user.two_fa_enabled and user.factor is not None and user.factor != '':
            if user.factor_passed:
                user.factor_passed = False
                user.save()
                return redirect("/authentication/two-factor")