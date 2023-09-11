

def enable_two_factor(strategy, user, *args, **kwargs):
    if user and user.is_authenticated:
        if user.two_fa_enabled and user.factor is not None and user.factor != '':
            if user.factor_passed:
                user.factor_passed = False
                user.save()
                return