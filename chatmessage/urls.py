from django.urls import path
from . import views


urlpatterns = [
    path('chatmessage/<int:sender_id>/<int:contact_id>/<str:sender_type>/', views.chat, name='chat_message')
    ]
