from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.PatientSignUpView.as_view(), name='signup'),
    path('login/', views.PatientLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('profile/update/', views.PatientProfileUpdateView.as_view(), name='profile_update'),
]