from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Measure(models.Model):    
    datetime = models.DateTimeField() # Should it be unique ?
    co2_rate = models.PositiveSmallIntegerField()


class InterpolateMeasure(Measure):
    # Add validator making sure %M:%S
    pass 
