from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .forms import MessageForm
from users.models import Patient, Doctor

User = get_user_model()


@login_required
def conversation_list(request):
    user = request.user

    if user.role == 'PATIENT':
        try:
            patient = user.patient
            conversations = Conversation.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            conversations = []
    elif user.role == 'DOCTOR':
        try:
            doctor = user.doctor
            conversations = Conversation.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            conversations = []
    else:
        conversations = []

    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations
    })


@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    user = request.user

    # 确定患者和医生
    if user.role == 'PATIENT' and other_user.role == 'DOCTOR':
        patient = user.patient
        doctor = other_user.doctor
    elif user.role == 'DOCTOR' and other_user.role == 'PATIENT':
        doctor = user.doctor
        patient = other_user.patient
    else:
        return redirect('conversation_list')

    # 获取或创建对话
    conversation, created = Conversation.objects.get_or_create(
        patient=patient,
        doctor=doctor
    )

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    user = request.user

    # 安全检查 - 确保用户是此对话的一部分
    if (user.role == 'PATIENT' and user.patient != conversation.patient) or \
            (user.role == 'DOCTOR' and user.doctor != conversation.doctor):
        return redirect('conversation_list')

    # 将所有消息标记为已读
    if user.role == 'PATIENT':
        Message.objects.filter(conversation=conversation, sender=conversation.doctor.user, is_read=False).update(
            is_read=True)
    else:
        Message.objects.filter(conversation=conversation, sender=conversation.patient.user, is_read=False).update(
            is_read=True)

    # 处理新消息
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = user
            message.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    messages = conversation.messages.all()

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })


@login_required
def unread_message_count(request):
    user = request.user
    count = 0

    if user.role == 'PATIENT':
        try:
            patient = user.patient
            count = Message.objects.filter(
                conversation__patient=patient,
                sender__role='DOCTOR',
                is_read=False
            ).count()
        except Patient.DoesNotExist:
            pass
    elif user.role == 'DOCTOR':
        try:
            doctor = user.doctor
            count = Message.objects.filter(
                conversation__doctor=doctor,
                sender__role='PATIENT',
                is_read=False
            ).count()
        except Doctor.DoesNotExist:
            pass

    return JsonResponse({'count': count})


@login_required
def doctor_list(request):
    if request.user.role != 'PATIENT':
        return redirect('home')

    doctors = Doctor.objects.all()
    return render(request, 'messaging/doctor_list.html', {'doctors': doctors})