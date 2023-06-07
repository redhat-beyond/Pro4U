import pytest
from conftest import USER_INFORMATION, PROFILE_INFORMATION
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

    def test_get_professional_business_page(self, client, make_client, make_professional):
        test_client = make_client()
        client.force_login(test_client.profile_id.user_id)
        test_professional = make_professional(username=USER_INFORMATION.get('username')[1],
                                              password=USER_INFORMATION.get('password')[1],
                                              email=USER_INFORMATION.get('email')[1],
                                              phone_number=PROFILE_INFORMATION.get('phone_number')[1])
        response = client.get(f"{PROFILE_URL}professional/{test_professional.professional_id}/")
        assert response.status_code == 200
        assert 'account/business_page.html' in [template.name for template in response.templates]
        returned_professional = response.context.get("professional")
        assert returned_professional == test_professional
        assert f"{test_professional.profession}" in response.content.decode('utf-8')
        assert f"{test_professional.description}" in response.content.decode('utf-8')
        assert f"{test_professional.profile_id.user_id.first_name}" in response.content.decode('utf-8')
        assert f"{test_professional.profile_id.user_id.last_name}" in response.content.decode('utf-8')
