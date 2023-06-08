import pytest
from account.tests.urls_tests.test_general import PROFILE_URL


@pytest.mark.django_db
class TestProfessionalProfile:
    def test_get_professional_profile(self, client, make_professional):
        test_professional = make_professional()
        client.force_login(test_professional.profile_id.user_id)
        response = client.get(f"{PROFILE_URL}")
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{test_professional.profile_id.user_id.first_name}'s Profile" in response.content.decode('utf-8')
        assert 'Type Of Jobs' in response.content.decode('utf-8')
        assert 'Schedule' in response.content.decode('utf-8')
        assert 'img/blank_profile.png' in response.content.decode('utf-8')

    def test_profile_template_inheritance(self, client, make_professional):
        urls = ['settings/']
        test_professional = make_professional()
        client.force_login(test_professional.profile_id.user_id)

        for url in urls:
            response = client.get(f"{PROFILE_URL}{url}")
            assert 'account/profile.html' in [template.name for template in response.templates]

    def test_get_professional_profile_settings(self, client, make_professional):
        test_professional = make_professional()
        client.force_login(test_professional.profile_id.user_id)
        response = client.get(f"{PROFILE_URL}settings/")
        assert response.status_code == 200
        assert 'account/profile_details.html' in [template.name for template in response.templates]
        assert test_professional.profile_id.user_id.username in response.content.decode()
        assert test_professional.profile_id.user_id.first_name in response.content.decode()
        assert test_professional.profile_id.user_id.last_name in response.content.decode()
        assert test_professional.profile_id.user_id.email in response.content.decode()
        assert test_professional.profile_id.phone_number in response.content.decode()
        assert test_professional.profile_id.country in response.content.decode()
        assert test_professional.profile_id.city in response.content.decode()
        assert test_professional.profile_id.address in response.content.decode()
        assert test_professional.profession in response.content.decode()
        assert test_professional.description in response.content.decode()
