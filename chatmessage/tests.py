from .models import Chatmessage
import pytest

PROFESSIONAL_ID = "professional1"
CLIENT_ID = "client1"
MESSAGE = "message1"


@pytest.fixture
def chatmessage():
    return Chatmessage(professional_id=PROFESSIONAL_ID, client_id=CLIENT_ID, message=MESSAGE)


@pytest.fixture
def persisted_chatmessage(chatmessage):
    chatmessage.save()
    return [(chatmessage.message_id), (chatmessage.professional_id),
            (chatmessage.client_id), (chatmessage.date), (chatmessage.message)]


@pytest.mark.django_db
class TestChatmessageModel:
    def test_new_member(self, chatmessage):
        assert chatmessage.professional_id == PROFESSIONAL_ID
        assert chatmessage.client_id == CLIENT_ID
        assert chatmessage.message == MESSAGE

    def test_chatmessage(self, chatmessage):
        chatmessage.save()
        assert chatmessage in Chatmessage.objects.all()

    def test_del_chatmessage(self, chatmessage):
        chatmessage.save()
        chatmessage.delete()
        assert chatmessage not in Chatmessage.objects.all()

    def test_get_professional_contacts(self, persisted_chatmessage):
        assert [persisted_chatmessage[2]] == \
            Chatmessage.get_all_professional_contacts(professional_id=PROFESSIONAL_ID)

    def test_get_client_contacts(self, persisted_chatmessage):
        assert [persisted_chatmessage[1]] == \
            Chatmessage.get_all_client_contacts(client_id=CLIENT_ID)

    def get_chat_between_professional_and_client(self, persisted_chatmessage):
        assert persisted_chatmessage == \
            Chatmessage.objects.filter(professional_id=PROFESSIONAL_ID, client_id=CLIENT_ID)
