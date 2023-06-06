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
