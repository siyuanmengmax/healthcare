from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MedicalRecord
from .forms import MedicalRecordForm


@login_required
def upload_ehr(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = request.user.patient
            record.created_by = request.user
            record.save()
            return redirect('ehr_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'ehr/upload.html', {'form': form})


class PatientEHRListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'ehr/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient=self.request.user.patient).order_by('-creation_date')