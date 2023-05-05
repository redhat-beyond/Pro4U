from account.models.profile import Profile, UserType
from account.models.client import Client
from .test_profile import PROFILE_INFORMATION
from conftest import CLIENT_INFORMATION
import pytest


@pytest.mark.django_db
class TestClientModel:
    def test_new_client(self, make_client):
        client = make_client()
        assert client.birthday == CLIENT_INFORMATION.get('birthday')[0]

    def test_get_client(self, make_client):
        client = make_client()
        assert client in Client.objects.all()

    def test_delete_client(self, make_client):
        client = make_client()
        client.delete()
        assert client not in Client.objects.all()

    def test_delete_user_deletes_client(self, make_client):
        client = make_client()
        client.profile_id.delete()
        assert client not in Client.objects.all()

    def test_delete_client_deletes_profile(self, make_client):
        client = make_client()
        Client.delete_client(client_id=client.client_id)
        assert client.profile_id not in Profile.objects.all()

    def test_filter_by_city(self, make_client):
        client = make_client(username='professional11', password='password1', email='john.doe@example.com',
                             phone_number='111111', user_type=UserType.Client)
        make_client(username='client22', password='password2', city="Toronto",
                    email='john2.doe@example.com', phone_number='222222', user_type=UserType.Client)
        make_client(username='client33', password='password3', city="London",
                    email='john3.doe@example.com', phone_number='333333', user_type=UserType.Client)

        assert list(Client.filter_client_by_city(PROFILE_INFORMATION.get('city')[0])) == [client]
