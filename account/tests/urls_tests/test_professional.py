import pytest


BASE_URL = '/professional'
FAKE_ID = 222222222


@pytest.mark.django_db
class TestProfessionalProfile:
    def test_get_client_profile(self, client, make_professional):
        test_professional = make_professional()
        client.force_login(test_professional.profile_id.user_id)
        response = client.get(f"{BASE_URL}/profile/{test_professional.professional_id}/")
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{test_professional.profile_id.user_id.first_name}'s Profile" in response.content.decode('utf-8')

    def test_show_profile_non_existent_client(self, client):
        response = client.get(f"{BASE_URL}/profile/{FAKE_ID}/")
        assert response.status_code == 404

    def test_show_profile_static_files(self, client, make_professional):
        test_professional = make_professional()
        client.force_login(test_professional.profile_id.user_id)
        response = client.get(f"{BASE_URL}/profile/{test_professional.professional_id}/")
        assert 'img/blank_profile.png' in response.content.decode('utf-8')
