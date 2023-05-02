from account.models.profile import Profile
from account.models.client import Client
from .test_profile import CITY
from datetime import datetime
import pytest


BIRTHDAY = datetime(2000, 1, 1)


@pytest.fixture
def save_clients(client, client2):
    client.profile_id.user_id.save()
    client.profile_id.save()
    client.save()
    client2.profile_id.user_id.save()
    client2.profile_id.save()
    client2.save()


@pytest.mark.django_db
class TestClientModel:
    def test_new_client(self, client):
        assert client.birthday == BIRTHDAY

    def test_get_client(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        assert client in Client.objects.all()

    def test_delete_client(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        client.delete()
        assert client not in Client.objects.all()

    def test_delete_user_deletes_client(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        client.profile_id.delete()
        assert client not in Client.objects.all()

    def test_delete_client_deletes_profile(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        Client.delete_client(client_id=client.client_id)
        assert client.profile_id not in Profile.objects.all()

    def test_filter_by_city(self, save_clients, client):
        assert list(Client.filter_client_by_city(CITY)) == [client]
