from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Patient
from django.urls import reverse

User = get_user_model()


class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testpatient',
            email='test@example.com',
            password='securepassword123',
            role='PATIENT'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            name='Test Patient',
            date_of_birth='1990-01-01',
            phone='555-123-4567'
        )

    def test_user_registration(self):
        response = self.client.post('/signup/', {
            'username': 'newpatient',
            'email': 'new@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'name': 'New Patient',
            'date_of_birth': '1990-01-01',
            'phone': '555-123-0000'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after signup
        self.assertTrue(User.objects.filter(username='newpatient').exists())

    def test_patient_profile_view(self):
        self.client.login(username='testpatient', password='securepassword123')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Patient')

    def test_patient_model(self):
        self.assertEqual(str(self.patient), 'Test Patient')
        self.assertEqual(self.patient.user.username, 'testpatient')
