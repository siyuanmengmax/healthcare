from django.db import models
from users.models import Patient, User


class MedicalRecordTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MedicalRecord(models.Model):
    RECORD_TYPES = [
        ('History', 'Medical History'),
        ('Lab', 'Laboratory Report'),
        ('Prescription', 'Prescription'),
        ('Note', 'Medical Notes'),
        ('Imaging', 'Imaging Results'),
        ('Surgery', 'Surgical Report'),
        ('Consultation', 'Consultation Notes'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Archived', 'Archived'),
        ('Pending', 'Pending Review'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_records')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_records', null=True,
                                   blank=True)
    content = models.TextField(blank=True)
    attachments = models.FileField(upload_to='ehr_attachments/')
    description = models.CharField(max_length=255)
    tags = models.ManyToManyField(MedicalRecordTag, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    is_confidential = models.BooleanField(default=False, help_text="Mark as confidential to restrict access")

    def __str__(self):
        return f"{self.patient.name} - {self.get_record_type_display()} - {self.creation_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-creation_date']


class MedicalRecordAnalysis(models.Model):
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, related_name='analysis')
    analysis_text = models.TextField()
    diagnosis = models.JSONField(null=True, blank=True)
    medications = models.JSONField(null=True, blank=True)
    treatments = models.JSONField(null=True, blank=True)
    abnormal_values = models.JSONField(null=True, blank=True)
    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.medical_record}"