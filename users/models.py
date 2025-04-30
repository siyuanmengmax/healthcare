from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')
    account_status = models.CharField(max_length=20,
                                      choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended')],
                                      default='Active')

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.TextField(blank=True)
    insurance_info = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    office_address = models.TextField(blank=True)
    office_hours = models.TextField(blank=True)

    def __str__(self):
        return self.name