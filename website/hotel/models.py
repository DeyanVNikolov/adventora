import uuid

from django.db import models
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _


class Hotel(models.Model):
    uid = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    address_text = models.CharField(max_length=100, null=True, blank=True, default="NONE")
    address_confirmed = models.BooleanField(default=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=50000, default=_("No description provided."))
    EIK = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='owner')
    mol_name = models.CharField(max_length=100, null=True, blank=True)
    stars = models.IntegerField(null=True)
    approved = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'hotel'
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"


class Room(models.Model):

    uid = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4, unique=True)
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='hotel_room')
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='room_images', null=True, blank=True)
    luxuries = models.ManyToManyField('LuxuryOption', blank=True, related_name='rooms')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class LuxuryOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name