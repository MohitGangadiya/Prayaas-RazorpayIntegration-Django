# Importing necessary modules
from django.contrib import admin

# Registering model
from .models import Donor
admin.site.register(Donor)