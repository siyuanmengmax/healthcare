from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient


class PatientSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=200, label='Name')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False,
                                    label='Date of Birth')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Address')
    phone = forms.CharField(max_length=20, required=False, label='Phone')
    emergency_contact = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False,
                                        label='Emergency Contact')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'PATIENT'
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                name=self.cleaned_data.get('name'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                address=self.cleaned_data.get('address'),
                phone=self.cleaned_data.get('phone'),
                emergency_contact=self.cleaned_data.get('emergency_contact')
            )
        return user


class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'address', 'phone', 'emergency_contact']
        labels = {
            'name': 'Name',
            'date_of_birth': 'Date of Birth',
            'address': 'Address',
            'phone': 'Phone',
            'emergency_contact': 'Emergency Contact',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'emergency_contact': forms.Textarea(attrs={'rows': 3}),
        }