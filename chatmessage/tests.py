from .models import Chatmessage, SenderType
import pytest


MESSAGE = "message1"


@pytest.fixture
def persisted_chatmessage(chatmessage):
    chatmessage.save()
    return [(chatmessage.message_id), (chatmessage.professional_id),
            (chatmessage.client_id), (chatmessage.date), (chatmessage.message), (chatmessage.sender_type)]


@pytest.mark.django_db
class TestChatmessageModel:
    def test_new_member(self, chatmessage, professional, client):
        assert chatmessage.professional_id == professional
        assert chatmessage.client_id == client
        assert chatmessage.message == MESSAGE
        assert chatmessage.sender_type == SenderType.Client

    def test_chatmessage(self, chatmessage):
        chatmessage.save()
        assert chatmessage in Chatmessage.objects.all()

    def test_del_chatmessage(self, chatmessage):
        chatmessage.save()
        chatmessage.delete()
        assert chatmessage not in Chatmessage.objects.all()

    def test_get_professional_contacts(self, persisted_chatmessage, professional):
        assert [persisted_chatmessage[2]] == \
            Chatmessage.get_all_professional_contacts(professional_id=professional)

    def test_get_client_contacts(self, persisted_chatmessage, client):
        assert [persisted_chatmessage[1]] == \
            Chatmessage.get_all_client_contacts(client_id=client)

    def get_chat_between_professional_and_client(self, persisted_chatmessage, professional, client):
        assert persisted_chatmessage == \
            Chatmessage.objects.filter(professional_id=professional, client_id=client)
