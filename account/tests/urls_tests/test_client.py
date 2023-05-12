import pytest
from .test_profile import TestProfileViews


BASE_URL = '/client'


@pytest.mark.django_db
class TestClientViews:
    def test_get_client_profile(self, client, demo_client):
        TestProfileViews.get_profile(client=client, entity_id=demo_client.client_id, url=BASE_URL)
