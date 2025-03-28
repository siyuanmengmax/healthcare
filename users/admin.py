from django.contrib import admin
from .models import User, Patient

admin.site.register(User)
admin.site.register(Patient)