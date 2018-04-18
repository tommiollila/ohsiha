from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date

class Person(models.Model):
    email = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(default=date.today)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)

class TrafficLightDetectors(models.Model):
    detector = models.CharField(max_length=25, default='')
    device = models.CharField(max_length=25, default='')
    intersection = models.CharField(max_length=25, default='')
    traffic_amount = models.IntegerField(blank=True, null=True, default=None)
    realiable_value = models.IntegerField(blank=True, null=True, default=None)
    congestion_count = models.IntegerField(blank=True, null=True, default=None)
    queue_length = models.IntegerField(blank=True, null=True, default=None)
    vehicle_count = models.IntegerField(blank=True, null=True, default=None)
    wait_time_max = models.FloatField(blank=True, null=True, default=None)
    wait_time_avg = models.FloatField(blank=True, null=True, default=None)
    latitude = models.FloatField(blank=True, null=True, default=None)
    longitude = models.FloatField(blank=True, null=True, default=None)
    street_name = models.CharField(max_length=100, blank=True, null=True, default=None)

    def __str__(self):
        return self.detector

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
