from .models import Chatmessage
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_chat(client, professional, demo_client):
    contact_id = professional.professional_id
    sender_id = demo_client.client_id
    sender_type = 'C'
    url = reverse('chat_message', args=[sender_id, contact_id, sender_type])
    response = client.get(url)
    assert response.status_code == 200
    assert 'chatmessage/message.html' in response.templates[0].name


@pytest.mark.django_db
def test_send_message_from_professional_to_client(client, professional, demo_client):
    contact_id = demo_client.client_id
    sender_id = professional.professional_id
    sender_type = 'P'

    post_data = {
        'msg_sent': 'Test message!',
    }

    url = reverse('chat_message', args=[sender_id, contact_id, sender_type])
    response = client.post(url, post_data)

    assert response.status_code == 200

    last_message_in_chat = Chatmessage.get_chat_between_professional_and_client(
        professional_id=professional,
        client_id=demo_client
    ).latest('date')

    assert last_message_in_chat.message == 'Test message!'


@pytest.mark.django_db
def test_send_message_from_client_to_professional(client, professional, demo_client):
    contact_id = professional.professional_id
    sender_id = demo_client.client_id
    sender_type = 'C'

    post_data = {
        'msg_sent': 'Test message!',
    }

    url = reverse('chat_message', args=[sender_id, contact_id, sender_type])
    response = client.post(url, post_data)

    assert response.status_code == 200

    last_message_in_chat = Chatmessage.get_chat_between_professional_and_client(
        professional_id=professional,
        client_id=demo_client
    ).latest('date')

    assert last_message_in_chat.message == 'Test message!'


@pytest.mark.django_db
def test_cant_send_empty_message(client, professional, demo_client):
    contact_id = demo_client.client_id
    sender_id = professional.professional_id
    sender_type = 'P'

    url = reverse('chat_message', args=[sender_id, contact_id, sender_type])

    post_data = {
        'msg_sent': 'The message sent before the empty message',
    }

    response = client.post(url, post_data)
    assert response.status_code == 200

    post_data = {
        'msg_sent': '',
    }

    response = client.post(url, post_data)
    assert response.status_code == 200

    # Retrieve the last message in the chat
    chat_messages = Chatmessage.get_chat_between_professional_and_client(
        professional_id=professional,
        client_id=demo_client
    ).order_by('-date')

    # Verify the last message
    assert chat_messages.count() == 1
    last_message_in_chat = chat_messages[0]
    assert last_message_in_chat.message == 'The message sent before the empty message'
