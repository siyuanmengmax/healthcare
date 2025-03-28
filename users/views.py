from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from .forms import PatientSignUpForm, PatientProfileUpdateForm
from .models import Patient


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


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


class PatientLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('patient_profile')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return form


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