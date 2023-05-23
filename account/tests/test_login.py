import pytest
from django.urls import reverse


USERNAME = "testusername3"
PASSWORD = 'testpassword3'


@pytest.mark.django_db
class TestLoginView:
    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def test_sign_in_POST_valid(self, client, professional):
        response = client.post('/login/', {
            'username': USERNAME,
            'password': PASSWORD,
        })
        assert response.status_code == 302
        assert response.url == reverse('professional_urls:show_profile', args=[professional.pk])

    def test_sign_in_POST_invalid(self, client):
        response = client.post('/login/', {
            'username': "test2",
            'password': PASSWORD,
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.content
