import pytest
from .test_profile import TestProfileViews, FAKE_ID


BASE_URL = '/client'


@pytest.mark.django_db
class TestClientViews:
    def test_get_client_profile(self, client, demo_client):
        test_client = demo_client
        response = TestProfileViews.get_profile(client=client, entity_id=test_client.client_id, url=BASE_URL)
        assert response.status_code == 200
        assert 'account/client_profile.html' in [template.name for template in response.templates]
        assert f"{test_client.profile_id.user_id.first_name}'s Profile" in response.content.decode('utf-8')

    def test_show_profile_non_existent_client(self, client, demo_client):
        response = TestProfileViews.get_profile(client=client, entity_id=FAKE_ID, url=BASE_URL)
        assert response.status_code == 404

    def test_show_profile_template_inheritance(self, client, demo_client):
        test_client = demo_client
        response = TestProfileViews.get_profile(client=client, entity_id=test_client.client_id, url=BASE_URL)
        assert 'account/profile.html' in [template.name for template in response.templates]

    def test_show_profile_static_files(self, client, demo_client):
        test_client = demo_client
        response = TestProfileViews.get_profile(client=client, entity_id=test_client.client_id, url=BASE_URL)
        assert 'img/blank_profile.png' in response.content.decode('utf-8')
