from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_ehr, name='ehr_upload'),
    path('list/', views.PatientEHRListView.as_view(), name='ehr_list'),
    path('record/<int:pk>/', views.EHRDetailView.as_view(), name='ehr_detail'),
    path('record/<int:pk>/update/', views.update_ehr, name='ehr_update'),
    path('record/<int:pk>/delete/', views.delete_ehr, name='ehr_delete'),
    path('add-tag/', views.add_tag, name='add_tag'),
    path('patients/<int:patient_id>/records/', views.DoctorPatientEHRListView.as_view(), name='patient_records'),
    path('record/<int:pk>/analyze/', views.analyze_medical_record, name='analyze_medical_record'),
    path('record/<int:pk>/analysis/', views.view_analysis, name='ehr_analysis_detail'),
]