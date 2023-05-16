from .test_profile import TestProfileViews
import pytest

BASE_URL = '/professional'


@pytest.mark.django_db
class TestProfessionalViews:
    def test_get_professional_profile(self, client, professional):
        TestProfileViews.get_profile(client=client, entity_id=professional.professional_id, url=BASE_URL)
