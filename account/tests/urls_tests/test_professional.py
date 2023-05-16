import pytest
from .test_profile import TestProfileViews, FAKE_ID


BASE_URL = '/professional'


@pytest.mark.django_db
class TestClientViews:
    def test_get_client_profile(self, client, professional):
        test_professional = professional
        response = TestProfileViews.get_profile(client=client, entity_id=test_professional.professional_id,
                                                url=BASE_URL)
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{test_professional.profile_id.user_id.first_name}'s Profile" in response.content.decode('utf-8')

    def test_show_profile_non_existent_professional(self, client, professional):
        response = TestProfileViews.get_profile(client=client, entity_id=FAKE_ID, url=BASE_URL)
        assert response.status_code == 404

    def test_show_profile_static_files(self, client, professional):
        test_professional = professional
        response = TestProfileViews.get_profile(client=client, entity_id=test_professional.professional_id,
                                                url=BASE_URL)
        assert 'img/blank_profile.png' in response.content.decode('utf-8')
