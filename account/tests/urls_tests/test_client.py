import pytest
from account.tests.urls_tests.test_general import PROFILE_URL
from django.urls import reverse
from conftest import USER_INFORMATION, PROFILE_INFORMATION


@pytest.fixture
def save_client(make_client):
    new_client = make_client()
    new_client.profile_id.user_id.save()
    new_client.profile_id.save()
    new_client.save()
    return new_client


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

    def test_profile_template_inheritance(self, client, make_client):
        urls = ['settings/']
        test_client = make_client()
        client.force_login(test_client.profile_id.user_id)

        for url in urls:
            response = client.get(f"{PROFILE_URL}{url}")
            assert 'account/profile.html' in [template.name for template in response.templates]

    def test_get_client_profile_settings(self, client, make_client):
        test_client = make_client()
        client.force_login(test_client.profile_id.user_id)
        response = client.get(f"{PROFILE_URL}settings/")
        assert response.status_code == 200
        assert 'account/profile_details.html' in [template.name for template in response.templates]
        assert test_client.profile_id.user_id.username in response.content.decode()
        assert test_client.profile_id.user_id.first_name in response.content.decode()
        assert test_client.profile_id.user_id.last_name in response.content.decode()
        assert test_client.profile_id.user_id.email in response.content.decode()
        assert test_client.profile_id.phone_number in response.content.decode()
        assert test_client.profile_id.country in response.content.decode()
        assert test_client.profile_id.city in response.content.decode()
        assert test_client.profile_id.address in response.content.decode()
        assert 'Jan. 1, 2000' in response.content.decode()

    def test_get_client_profile_edit(self, client, save_client):
        client.force_login(save_client.profile_id.user_id)
        response = client.get(f"{PROFILE_URL}edit/")
        assert response.status_code == 200
        assert 'account/edit_profile.html' in [template.name for template in response.templates]

        data = {
            'username': USER_INFORMATION.get('username')[1],
            'first_name': USER_INFORMATION.get('first_name')[1],
            'last_name': USER_INFORMATION.get('last_name')[1],
            'email': USER_INFORMATION.get('email')[1],
            'phone_number': PROFILE_INFORMATION.get('phone_number')[1],
            'country': PROFILE_INFORMATION.get('country')[1],
            'city': PROFILE_INFORMATION.get('city')[1],
            'address': PROFILE_INFORMATION.get('address')[1]
        }
        response = client.post(f"{PROFILE_URL}edit/", data)
        assert response.status_code == 302
        save_client.refresh_from_db()
        assert save_client.profile_id.user_id.username == USER_INFORMATION.get('username')[1]
        assert save_client.profile_id.user_id.first_name == USER_INFORMATION.get('first_name')[1]
        assert save_client.profile_id.user_id.last_name == USER_INFORMATION.get('last_name')[1]
        assert save_client.profile_id.user_id.email == USER_INFORMATION.get('email')[1]
        assert save_client.profile_id.phone_number == PROFILE_INFORMATION.get('phone_number')[1]
        assert save_client.profile_id.country == PROFILE_INFORMATION.get('country')[1]
        assert save_client.profile_id.city == PROFILE_INFORMATION.get('city')[1]
        assert save_client.profile_id.address == PROFILE_INFORMATION.get('address')[1]
        assert response.url == reverse('show_settings')

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
        assert f"{test_professional.get_profession_display()}" in response.content.decode('utf-8')
        assert f"{test_professional.description}" in response.content.decode('utf-8')
        assert f"{test_professional.profile_id.user_id.first_name}" in response.content.decode('utf-8')
        assert f"{test_professional.profile_id.user_id.last_name}" in response.content.decode('utf-8')
