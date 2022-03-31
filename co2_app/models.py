from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Measure(models.Model):    
    date_time = models.DateTimeField() # Should it be unique ?
    co2_rate = models.PositiveSmallIntegerField()


class InterpolateData(models.Model):
    # Wanted to inherit from Measure but not compatible with bulk.create()    
    date_time = models.DateTimeField() # Should it be unique ?
    co2_rate = models.PositiveSmallIntegerField()
