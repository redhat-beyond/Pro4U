from account.models.profile import Profile
from account.models.professional import Professions, Professional
from .test_profile import CITY
from .test_profile import FIRST_NAME
from .test_profile import LAST_NAME
import pytest


PROFESSION = Professions.Locksmith
DESCRIPTION = 'I'


@pytest.fixture
def save_professionals(professional, professional2, professional3):
    professional.profile_id.user_id.save()
    professional.profile_id.save()
    professional.save()
    professional2.profile_id.user_id.save()
    professional2.profile_id.save()
    professional2.save()
    professional3.profile_id.user_id.save()
    professional3.profile_id.save()
    professional3.save()


@pytest.mark.django_db
class TestProfessionalModel:
    def test_new_professional(self, professional):
        assert professional.profession == PROFESSION
        assert professional.description == DESCRIPTION

    def test_get_professional(self, professional):
        professional.profile_id.user_id.save()
        professional.profile_id.save()
        professional.save()
        assert professional in Professional.objects.all()

    def test_delete_professional(self, professional):
        professional.profile_id.user_id.save()
        professional.profile_id.save()
        professional.save()
        professional.delete()
        assert professional not in Professional.objects.all()

    def test_delete_user_deletes_professional(self, professional):
        professional.profile_id.user_id.save()
        professional.profile_id.save()
        professional.save()
        professional.profile_id.delete()
        assert professional not in Professional.objects.all()

    def test_delete_professional_deletes_profile(self, professional):
        professional.profile_id.user_id.save()
        professional.profile_id.save()
        professional.save()
        Professional.delete_professional(professional_id=professional.professional_id)
        assert professional.profile_id not in Profile.objects.all()

    def test_filter_by_profession(self, save_professionals, professional, professional3):
        assert list(Professional.filter_by_profession(PROFESSION)) == [professional, professional3]

    def test_filter_by_city(self, save_professionals, professional3):
        assert list(Professional.filter_professionals_by_city(CITY)) == [professional3]

    def test_filter_by_first_name(self, save_professionals, professional, professional3):
        assert list(Professional.filter_professionals_by_first_name(FIRST_NAME)) == [professional, professional3]

    def test_filter_by_last_name(self, save_professionals, professional, professional3):
        assert list(Professional.filter_professionals_by_last_name(LAST_NAME)) == [professional, professional3]
