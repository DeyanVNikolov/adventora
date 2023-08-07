import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    website = models.CharField(max_length=100)
    description = models.TextField()
    EIK = models.CharField(max_length=50)
    ownerid = models.CharField(max_length=50)
    stars = models.IntegerField()


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
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.username
