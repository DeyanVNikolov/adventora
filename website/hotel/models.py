import uuid

from django.db import models


class Hotel(models.Model):
    unique_id = models.CharField(max_length=100, null=True, blank=True, default=str(uuid.uuid4()))
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    address_text = models.CharField(max_length=100, null=True, blank=True, default="NONE")
    address_confirmed = models.BooleanField(default=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    EIK = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='owner')
    mol_name = models.CharField(max_length=100, null=True, blank=True)
    stars = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

