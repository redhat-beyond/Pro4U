from django.urls import path
from . import views


urlpatterns = [
    path('chatmessage/<int:contact_id>/', views.chat, name='chat_message'),
    path('chatmessage/', views.all_chats , name='all_chats')
    ]
