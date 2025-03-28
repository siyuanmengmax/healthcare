from django.db import models
from users.models import Patient, User


class MedicalRecord(models.Model):
    RECORD_TYPES = [
        ('History', 'Medical History'),
        ('Lab', 'Laboratory Report'),
        ('Prescription', 'Prescription'),
        ('Note', 'Medical Notes'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField(blank=True)
    attachments = models.FileField(upload_to='ehr_attachments/')
    description = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.patient.name} - {self.get_record_type_display()} - {self.creation_date.strftime('%Y-%m-%d')}"