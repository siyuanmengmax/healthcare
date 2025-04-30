from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('unread/count/', views.unread_message_count, name='unread_message_count'),
    path('doctors/', views.doctor_list, name='doctor_list'),
]