from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView
from .forms import PatientSignUpForm, PatientProfileUpdateForm, DoctorSignUpForm
from .models import Patient, Doctor


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        # 根据用户角色确定登录后的重定向页面
        if self.request.user.role == 'PATIENT':
            return reverse_lazy('patient_profile')
        elif self.request.user.role == 'DOCTOR':
            return reverse_lazy('doctor_profile')
        else:
            return reverse_lazy('home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return form

class PatientSignUpView(View):
    def get(self, request):
        form = PatientSignUpForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'users/signup.html', {'form': form})


class PatientProfileView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'users/profile.html'
    context_object_name = 'patient'

    def get_object(self):
        return self.request.user.patient


class PatientProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('patient_profile')

    def get_object(self):
        return self.request.user.patient

class DoctorSignUpView(View):
    def get(self, request):
        form = DoctorSignUpForm()
        return render(request, 'users/doctor_signup.html', {'form': form})

    def post(self, request):
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'users/doctor_signup.html', {'form': form})

class DoctorProfileView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'users/doctor_profile.html'
    context_object_name = 'doctor'

    def get_object(self):
        return self.request.user.doctor

class DoctorProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    fields = ['name', 'specialization', 'license_number', 'contact_number', 'bio', 'office_address', 'office_hours']
    template_name = 'users/doctor_profile_update.html'
    success_url = reverse_lazy('doctor_profile')

    def get_object(self):
        return self.request.user.doctor


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'users/patient_list.html'
    context_object_name = 'patients'

    def dispatch(self, request, *args, **kwargs):
        # 确保只有医生可以访问此视图
        if request.user.role != 'DOCTOR':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'users/patient_detail.html'
    context_object_name = 'patient'

    def dispatch(self, request, *args, **kwargs):
        # 确保只有医生可以访问此视图
        if request.user.role != 'DOCTOR':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)