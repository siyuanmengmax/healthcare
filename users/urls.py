from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.PatientSignUpView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('profile/update/', views.PatientProfileUpdateView.as_view(), name='profile_update'),
    path('doctor/signup/', views.DoctorSignUpView.as_view(), name='doctor_signup'),
    path('doctor/profile/', views.DoctorProfileView.as_view(), name='doctor_profile'),
    path('doctor/profile/update/', views.DoctorProfileUpdateView.as_view(), name='doctor_profile_update'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('login-history/', views.LoginHistoryView.as_view(), name='login_history'),
]