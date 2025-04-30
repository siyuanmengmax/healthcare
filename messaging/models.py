from django.db import models
from django.contrib.auth import get_user_model
from users.models import Patient, Doctor

User = get_user_model()


class Conversation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='conversations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['patient', 'doctor']

    def __str__(self):
        return f"Conversation between {self.patient.name} and Dr. {self.doctor.name}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"