from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Patient
from ehr.models import MedicalRecord  # Adjust import if model lives elsewhere
from django.core.files.uploadedfile import SimpleUploadedFile  # Add this to imports if not already
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class EHRTests(TestCase):

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
        self.client.login(username='testpatient', password='securepassword123')

    def test_ehr_upload(self):
        test_file = SimpleUploadedFile("sample_record.pdf", b"dummy content", content_type="application/pdf")
        response = self.client.post('/ehr/upload/', {
            'record_type': 'Lab',
            'description': 'Test Lab Report',
            'content': 'Lab results show normal values',
            'attachments': test_file
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MedicalRecord.objects.filter(description='Test Lab Report').exists())

class MedicalRecordModelTest(TestCase):

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

    def test_medical_record_creation(self):
        test_file = SimpleUploadedFile("testfile.pdf", b"file_content", content_type="application/pdf")

        record = MedicalRecord.objects.create(
            patient=self.patient,
            record_type='Lab',
            created_by=self.user,
            content='Some lab results text.',
            attachments=test_file,
            description='Lab Report April'
        )

        self.assertEqual(record.record_type, 'Lab')
        self.assertEqual(record.get_record_type_display(), 'Laboratory Report')
        self.assertEqual(record.patient.name, 'Test Patient')
        self.assertEqual(record.created_by.username, 'testpatient')
        self.assertEqual(record.description, 'Lab Report April')
        self.assertTrue(record.attachments.name.startswith('ehr_attachments/testfile'))
        self.assertTrue(record.__str__().startswith("Test Patient - Laboratory Report - "))