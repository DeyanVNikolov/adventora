import uuid

from django.db import models
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _


class Hotel(models.Model):
    id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=5000, null=True, blank=True)
    address_text = models.CharField(max_length=100, null=True, blank=True, default="NONE")
    address_confirmed = models.BooleanField(default=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=50001, default=_("No description provided."))
    EIK = models.CharField(max_length=50, null=True, blank=True)
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

    id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True)
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='rooms')
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    occupied = models.BooleanField(default=False)
    occupied_by = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='room_images', null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class LuxuryOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name