import pytest


PROFILE_URL = '/profile/'


@pytest.mark.django_db
class TestGeneral:
    def test_get_not_registered_entity(self, client):
        urls = ['']
        for url in urls:
            response = client.get(f"{PROFILE_URL}{url}")
            assert response.status_code == 200
            assert 'landing/homepage.html' in [template.name for template in response.templates]
