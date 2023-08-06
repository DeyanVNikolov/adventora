from django.contrib import admin

# Register your models here.


# register models
from .models import CustomUser

admin.site.register(CustomUser)