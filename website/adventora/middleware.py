import datetime

from django.shortcuts import redirect, reverse


class CheckRole:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.banned is True and not request.path.startswith("/authentication/banned"):
                return redirect("/authentication/banned")
            if request.path.startswith("/authentication/banned") and request.user.banned is False:
                return redirect("/")

            if request.user.two_fa_enabled is True and request.user.factor_passed is False and request.path.startswith("/authentication/two-factor") is False:
                if request.path.startswith('/authentication/logout'):
                    pass
                else:
                    return redirect("/authentication/two-factor")

            if not request.path.startswith("/authentication"):
                if not request.path.startswith("/lang/setlang/"):
                    if request.user.role is None or request.user.role.strip() == "" or request.user.confirmedrole is False:
                        return redirect("/authentication/choose-role")
                    elif request.user.first_name.strip() == "" or request.user.last_name.strip() == "" or request.user.first_name is None or request.user.last_name is None or request.user.confirmedname is False:
                        return redirect("/authentication/complete-name")
                    elif request.user.citizenship is None or request.user.citizenship == "" or request.user.confirmedcitizenship is False:
                        return redirect("/authentication/complete-citizenship")
                    elif request.user.email.strip() == "" or request.user.email is None or request.user.confirmedemail is False:
                        return redirect("/authentication/complete-email")
                    elif request.user.phone is None or request.user.phone == "" or request.user.confirmedphone is False:
                        return redirect("/authentication/complete-phone")
                    elif request.user.username.strip() == "" or request.user.username is None or request.user.confirmedusername is False:
                        return redirect("/authentication/complete-username")


        response = self.get_response(request)
        return response

