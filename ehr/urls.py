from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_ehr, name='ehr_upload'),
    path('list/', views.PatientEHRListView.as_view(), name='ehr_list'),
]