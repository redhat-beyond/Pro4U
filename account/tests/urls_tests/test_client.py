import pytest
from account.tests.urls_tests.test_general import PROFILE_URL


@pytest.mark.django_db
class TestClientProfile:
    def test_get_client_profile(self, client, make_client):
        test_client = make_client()
        client.force_login(test_client.profile_id.user_id)
        response = client.get(f"{PROFILE_URL}")
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{test_client.profile_id.user_id.first_name}'s Profile" in response.content.decode('utf-8')
        assert 'Search' in response.content.decode('utf-8')
        assert 'img/blank_profile.png' in response.content.decode('utf-8')
