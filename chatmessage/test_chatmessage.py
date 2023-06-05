from .models import Chatmessage
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_chat(client, professional, make_client):
    client1 = make_client()
    client.force_login(client1.profile_id.user_id)
    contact_id = professional.professional_id
    url = reverse('chat_message', args=[contact_id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'chatmessage/message.html' in response.templates[0].name


@pytest.mark.django_db
def test_send_message_from_professional_to_client(client, professional, make_client):
    client1 = make_client()
    client.force_login(professional.profile_id.user_id)
    contact_id = client1.client_id

    post_data = {
        'msg_sent': 'Test message!',
    }

    url = reverse('chat_message', args=[contact_id])
    response = client.post(url, post_data)

    assert response.status_code == 200

    last_message_in_chat = Chatmessage.get_chat_between_professional_and_client(
        professional_id=professional,
        client_id=client1
    ).latest('date')

    assert last_message_in_chat.message == 'Test message!'


@pytest.mark.django_db
def test_send_message_from_client_to_professional(client, professional, make_client):
    client1 = make_client()
    client.force_login(client1.profile_id.user_id)
    contact_id = professional.professional_id

    post_data = {
        'msg_sent': 'Test message!',
    }

    url = reverse('chat_message', args=[contact_id])
    response = client.post(url, post_data)

    assert response.status_code == 200

    last_message_in_chat = Chatmessage.get_chat_between_professional_and_client(
        professional_id=professional,
        client_id=client1
    ).latest('date')

    assert last_message_in_chat.message == 'Test message!'


@pytest.mark.django_db
def test_cant_send_empty_message(client, professional, make_client):
    client1 = make_client()
    client.force_login(professional.profile_id.user_id)
    contact_id = client1.client_id

    url = reverse('chat_message', args=[contact_id])

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
        client_id=client1
    ).order_by('-date')

    # Verify the last message
    assert chat_messages.count() == 1
    last_message_in_chat = chat_messages[0]
    assert last_message_in_chat.message == 'The message sent before the empty message'


@pytest.mark.django_db
def test_all_chats(client, professional, make_client):
    url = reverse('all_chats')

    client1 = make_client()
    client.force_login(professional.profile_id.user_id)
    response = client.get(url)

    assert response.status_code == 200
    assert 'chatmessage/message.html' in response.templates[0].name

    chat = response.context['chat']
    contacts = Chatmessage.get_all_client_contacts(client1)
    assert chat == contacts

    professional_user = professional.profile_id.user_id
    client.force_login(professional_user)
    response = client.get(url)

    assert response.status_code == 200
    assert 'chatmessage/message.html' in response.templates[0].name

    chat = response.context['chat']
    contacts = Chatmessage.get_all_professional_contacts(professional)
    assert chat == contacts
