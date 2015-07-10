from datetime import date, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    birthday = models.DateField(help_text="Please use MM/DD/YYYY format.")
    #phone = us.PhoneNumberField(blank=True, null=True)
    city = models.CharField(max_length=35)
    state = models.CharField("State/Province", max_length=32)  # us.USStateField()
    #country = models.ForeignKey(Country)
    registered_on = models.DateField("Registered on", auto_now_add=True)
    active = models.BooleanField(default=True)