from django import forms
from .models import MedicalRecord

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['record_type', 'content', 'attachments', 'description']
        labels = {
            'record_type': 'Record Type',
            'content': 'Content',
            'attachments': 'Attachments',
            'description': 'Description'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'description': forms.TextInput(attrs={'placeholder': 'Please briefly describe this record'})
        }