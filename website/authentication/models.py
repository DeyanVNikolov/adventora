import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):

    ROLE_CHOICES = (('user', 'User'), ('manager', 'Manager'), ("employee", "Employee"), ("admin", "Admin"),)

    uniqueid = models.CharField(max_length=100, null=True, blank=True, default=str(uuid.uuid4()))
    banned = models.BooleanField(default=False, null=True, blank=True)
    confirmedusername = models.BooleanField(default=False, null=True, blank=True)
    confirmedemail = models.BooleanField(default=False, null=True, blank=True)
    confirmedname = models.BooleanField(default=False, null=True, blank=True)
    confirmedrole = models.BooleanField(default=False, null=True, blank=True)
    confirmedcitizenship = models.BooleanField(default=False, null=True, blank=True)
    confirmedphone = models.BooleanField(default=False, null=True, blank=True)

    verifiedemail = models.BooleanField(default=False, null=True, blank=True)

    two_fa_enabled = models.BooleanField(default=False, null=True, blank=True)
    factor = models.CharField(max_length=120, null=True, blank=True)
    factor_passed = models.BooleanField(default=False, null=True, blank=True)

    phone = PhoneNumberField(null=True, blank=True)
    citizenship = CountryField(blank_label='(select country)', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='hotel')

    def __str__(self):
        return self.username
