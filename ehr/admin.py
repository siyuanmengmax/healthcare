from django.contrib import admin
from .models import MedicalRecord, MedicalRecordTag, MedicalRecordAnalysis

admin.site.register(MedicalRecord)
admin.site.register(MedicalRecordTag)
admin.site.register(MedicalRecordAnalysis)