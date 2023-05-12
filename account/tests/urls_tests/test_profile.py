import pytest


@pytest.mark.django_db
class TestProfileViews:
    @staticmethod
    def get_profile(client, url, entity_id):
        response = client.get(f"{url}/profile/{entity_id}/")
        assert response.status_code == 200
