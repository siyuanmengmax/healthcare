# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from messaging.models import Conversation, Message
from users.models import Patient, Doctor

User = get_user_model()

class MessagingViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.patient_user = User.objects.create_user(username='patient', password='pass', role='PATIENT')
        self.doctor_user = User.objects.create_user(username='doctor', password='pass', role='DOCTOR')
        self.other_user = User.objects.create_user(username='other', password='pass', role='OTHER')

        self.patient = Patient.objects.create(user=self.patient_user)
        self.doctor = Doctor.objects.create(user=self.doctor_user)

        self.conversation = Conversation.objects.create(patient=self.patient, doctor=self.doctor)

    def test_conversation_list_patient(self):
        self.client.login(username='patient', password='pass')
        response = self.client.get(reverse('conversation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.conversation, response.context['conversations'])

    def test_conversation_list_doctor(self):
        self.client.login(username='doctor', password='pass')
        response = self.client.get(reverse('conversation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.conversation, response.context['conversations'])

    def test_conversation_list_invalid_user(self):
        self.client.login(username='other', password='pass')
        response = self.client.get(reverse('conversation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['conversations']), 0)

    def test_start_conversation_patient_to_doctor(self):
        self.client.login(username='patient', password='pass')
        response = self.client.get(reverse('start_conversation', args=[self.doctor_user.id]))
        self.assertRedirects(response, reverse('conversation_detail', args=[self.conversation.id]))



    def test_start_conversation_invalid(self):
            self.client.login(username='patient', password='pass')
            response = self.client.get(reverse('start_conversation', args=[self.other_user.id]))
            self.assertRedirects(response, reverse('conversation_list'))

    def test_conversation_detail_access(self):
        self.client.login(username='patient', password='pass')
        response = self.client.get(reverse('conversation_detail', args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)

    def test_conversation_detail_access_denied(self):
        self.client.login(username='other', password='pass')
        response = self.client.get(reverse('conversation_detail', args=[self.conversation.id]))
        self.assertRedirects(response, reverse('conversation_list'))

    def test_send_message(self):
        self.client.login(username='patient', password='pass')
        response = self.client.post(
            reverse('conversation_detail', args=[self.conversation.id]),
            {'content': 'Hello!', 'attachment': ''}
        )
        self.assertRedirects(response, reverse('conversation_detail', args=[self.conversation.id]))
        self.assertTrue(Message.objects.filter(content='Hello!').exists())

    def test_unread_message_count_for_patient(self):
        Message.objects.create(
            conversation=self.conversation,
            sender=self.doctor_user,
            content='Unread message',
            is_read=False
        )
        self.client.login(username='patient', password='pass')
        response = self.client.get(reverse('unread_message_count'))
        self.assertEqual(response.json()['count'], 1)

    def test_unread_message_count_for_doctor(self):
        Message.objects.create(
            conversation=self.conversation,
            sender=self.patient_user,
            content='Unread message',
            is_read=False
        )
        self.client.login(username='doctor', password='pass')
        response = self.client.get(reverse('unread_message_count'))
        self.assertEqual(response.json()['count'], 1)

    def test_doctor_list_for_patient(self):
        self.client.login(username='patient', password='pass')
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.doctor, response.context['doctors'])

    def test_doctor_list_for_non_patient(self):
        self.client.login(username='doctor', password='pass')
        response = self.client.get(reverse('doctor_list'))
        self.assertRedirects(response, reverse('home'))
