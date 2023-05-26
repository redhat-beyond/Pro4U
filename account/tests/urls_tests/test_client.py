import pytest


BASE_URL = '/client'
FAKE_ID = 10000000


@pytest.mark.django_db
class TestClientProfile:
    def test_get_client_profile(self, client, make_client):
        test_client = make_client()
        client.force_login(test_client.profile_id.user_id)
        response = client.get(f"{BASE_URL}/profile/{test_client.client_id}/")
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{test_client.profile_id.user_id.first_name}'s Profile" in response.content.decode('utf-8')

    def test_show_profile_non_existent_client(self, client):
        response = client.get(f"{BASE_URL}/profile/{FAKE_ID}/")
        assert response.status_code == 404

    def test_show_profile_static_files(self, client, make_client):
        test_client = make_client()
        client.force_login(test_client.profile_id.user_id)
        response = client.get(f"{BASE_URL}/profile/{test_client.client_id}/")
        assert 'img/blank_profile.png' in response.content.decode('utf-8')
