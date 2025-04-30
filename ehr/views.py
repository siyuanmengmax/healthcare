from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from .models import MedicalRecord, MedicalRecordTag, MedicalRecordAnalysis
from .services import ClaudeMedicalAnalyzer
from .forms import MedicalRecordForm
from users.models import Patient

class EHRDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'ehr/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        # 患者只能看到自己的记录
        if self.request.user.role == 'PATIENT':
            return MedicalRecord.objects.filter(patient=self.request.user.patient)
        # 医生可以看到所有记录
        return MedicalRecord.objects.all()

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

@login_required
def update_ehr(request, pk):
    # 获取记录，确保访问权限
    if request.user.role == 'PATIENT':
        record = get_object_or_404(MedicalRecord, pk=pk, patient=request.user.patient)
    else:
        record = get_object_or_404(MedicalRecord, pk=pk)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.updated_by = request.user
            updated_record.save()
            form.save_m2m()  # 保存标签关系
            return redirect('ehr_detail', pk=record.pk)
    else:
        form = MedicalRecordForm(instance=record)

    return render(request, 'ehr/update.html', {'form': form, 'record': record})


@login_required
def delete_ehr(request, pk):
    # 获取记录，确保访问权限
    if request.user.role == 'PATIENT':
        record = get_object_or_404(MedicalRecord, pk=pk, patient=request.user.patient)
    else:
        record = get_object_or_404(MedicalRecord, pk=pk)

    if request.method == 'POST':
        record.delete()
        return redirect('ehr_list')

    return render(request, 'ehr/delete.html', {'record': record})


@login_required
def add_tag(request):
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        if tag_name:
            tag, created = MedicalRecordTag.objects.get_or_create(name=tag_name)
            return JsonResponse({'success': True, 'id': tag.id, 'name': tag.name})
    return JsonResponse({'success': False})


class PatientEHRListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'ehr/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        queryset = MedicalRecord.objects.all()

        # 患者只能看到自己的记录
        if self.request.user.role == 'PATIENT':
            queryset = queryset.filter(patient=self.request.user.patient)

        # 根据记录类型筛选
        record_type = self.request.GET.get('record_type')
        if record_type:
            queryset = queryset.filter(record_type=record_type)

        # 根据标签筛选
        tag_id = self.request.GET.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset.order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_types'] = MedicalRecord.RECORD_TYPES
        context['all_tags'] = MedicalRecordTag.objects.all()
        context['selected_type'] = self.request.GET.get('record_type', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        return context


class DoctorPatientEHRListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'ehr/list.html'
    context_object_name = 'records'

    def dispatch(self, request, *args, **kwargs):
        # 确保只有医生可以访问此视图
        if request.user.role != 'DOCTOR':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')
        patient = get_object_or_404(Patient, pk=patient_id)

        queryset = MedicalRecord.objects.filter(patient=patient)

        # 根据记录类型筛选
        record_type = self.request.GET.get('record_type')
        if record_type:
            queryset = queryset.filter(record_type=record_type)

        # 根据标签筛选
        tag_id = self.request.GET.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset.order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_types'] = MedicalRecord.RECORD_TYPES
        context['all_tags'] = MedicalRecordTag.objects.all()
        context['selected_type'] = self.request.GET.get('record_type', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs.get('patient_id'))
        return context


@login_required
def analyze_medical_record(request, pk):
    # 获取记录，确保访问权限
    if request.user.role == 'PATIENT':
        record = get_object_or_404(MedicalRecord, pk=pk, patient=request.user.patient)
    else:
        record = get_object_or_404(MedicalRecord, pk=pk)

    # 使用Claude API分析文档
    analyzer = ClaudeMedicalAnalyzer()
    analysis_result = analyzer.analyze_medical_document(record)

    # 保存分析结果
    analysis = analyzer.save_analysis_result(record, analysis_result)

    if analysis:
        messages.success(request, "Medical record analyzed successfully.")
    else:
        messages.error(request, "Error analyzing medical record.")

    return redirect('ehr_analysis_detail', pk=record.pk)


@login_required
def view_analysis(request, pk):
    # 获取记录，确保访问权限
    if request.user.role == 'PATIENT':
        record = get_object_or_404(MedicalRecord, pk=pk, patient=request.user.patient)
    else:
        record = get_object_or_404(MedicalRecord, pk=pk)

    # 获取分析结果
    try:
        analysis = record.analysis
    except MedicalRecordAnalysis.DoesNotExist:
        return redirect('analyze_medical_record', pk=record.pk)

    return render(request, 'ehr/analysis_detail.html', {
        'record': record,
        'analysis': analysis
    })