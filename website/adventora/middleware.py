from django.shortcuts import redirect


class CheckRole:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # check if url is not in authentication app
            if not request.path.startswith("/authentication"):
                if request.user.role is None or request.user.role.strip() == "" or request.user.confirmedrole is False:
                    return redirect("/authentication/choose-role")
                elif request.user.first_name.strip() == "" or request.user.last_name.strip() == "" or request.user.first_name is None or request.user.last_name is None or request.user.confirmedname is False:
                    return redirect("/authentication/complete-name")
                elif request.user.email.strip() == "" or request.user.email is None or request.user.confirmedemail is False:
                    return redirect("/authentication/complete-email")
                elif request.user.username.strip() == "" or request.user.username is None or request.user.confirmedusername is False:
                    return redirect("/authentication/complete-username")


        response = self.get_response(request)
        return response