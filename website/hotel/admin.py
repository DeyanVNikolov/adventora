from django.contrib import admin

# Register your models here.


from .models import Hotel, Room, Reservation, Luxury

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Luxury)


