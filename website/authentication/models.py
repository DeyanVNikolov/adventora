from django.contrib.auth.models import AbstractUser
from django.db import models


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

    confirmedusername = models.BooleanField(default=False)
    confirmedemail = models.BooleanField(default=False)
    confirmedname = models.BooleanField(default=False)
    confirmedrole = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
