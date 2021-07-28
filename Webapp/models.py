# Importing necessary modules
from os import name
from django.db import models

# Creating Model (Database-Table)
class Donor(models.Model):
    date = models.DateField(default=0000-00-00)
    payment_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    number = models.CharField(max_length=10)
    anonymous = models.BooleanField(default=False)
    amount = models.FloatField(max_length=100000)
    paid = models.BooleanField(default=False)
    receipt = models.BooleanField(default=False)
