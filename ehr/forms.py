from django import forms
from .models import MedicalRecord, MedicalRecordTag


class MedicalRecordForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=MedicalRecordTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = MedicalRecord
        fields = ['record_type', 'content', 'attachments', 'description', 'tags', 'is_confidential']
        labels = {
            'record_type': 'Record Type',
            'content': 'Content',
            'attachments': 'Attachments',
            'description': 'Description',
            'tags': 'Tags',
            'is_confidential': 'Confidential'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'description': forms.TextInput(attrs={'placeholder': 'Please briefly describe this record'})
        }