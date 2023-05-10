from account.models.professional import Professional
from conftest import professional
# from django.test import Client
from fixtures.test import Client
import pytest


BASE_URL = '/client'
@pytest.mark.django_db
class TestFilmViews:
    def test_get_client_profile(self, client, demo_client):
        test_client = demo_client
        response = client.get(f"{BASE_URL}/profile/{test_client.client_id}/")
        assert response.status_code == 200
