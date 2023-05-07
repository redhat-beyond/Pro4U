from account.models.profile import Profile, UserType
from account.models.professional import Professions, Professional
from .test_profile import USER_INFORMATION
from .test_profile import PROFILE_INFORMATION
from conftest import PROFESSIONAL_INFORMATION
import pytest


@pytest.mark.django_db
class TestProfessionalModel:
    def test_new_professional(self, make_professional):
        professional = make_professional()
        assert professional.profession == PROFESSIONAL_INFORMATION.get('profession')[0]
        assert professional.description == PROFESSIONAL_INFORMATION.get('description')[0]

    def test_get_professional(self, make_professional):
        professional = make_professional()
        assert professional in Professional.objects.all()

    def test_delete_professional(self, make_professional):
        professional = make_professional()
        professional.delete()
        assert professional not in Professional.objects.all()

    def test_delete_user_deletes_professional(self, make_professional):
        professional = make_professional()
        professional.profile_id.delete()
        assert professional not in Professional.objects.all()

    def test_delete_professional_deletes_profile(self, make_professional):
        professional = make_professional()
        Professional.delete_professional(professional_id=professional.professional_id)
        assert professional.profile_id not in Profile.objects.all()

    def test_filter_by_profession(self, make_professional):
        professional = make_professional(username='professional11', password='password1', email='john.doe@example.com',
                                         phone_number='111111', user_type=UserType.Professional)
        professional2 = make_professional(username='professional22', password='password2',
                                          email='john2.doe@example.com', phone_number='222222',
                                          user_type=UserType.Professional)
        make_professional(username='professional33', password='password3', profession=Professions.Plumber,
                          email='john3.doe@example.com', phone_number='333333', user_type=UserType.Professional)

        assert list(Professional.filter_by_profession(PROFESSIONAL_INFORMATION.get('profession')[0])) ==\
               [professional, professional2]

    def test_filter_by_city(self, make_professional):
        professional = make_professional(username='professional11', password='password1', email='john.doe@example.com',
                                         phone_number='111111', user_type=UserType.Professional)
        make_professional(username='professional22', password='password2', city="Toronto",
                          email='john2.doe@example.com', phone_number='222222', user_type=UserType.Professional)
        make_professional(username='professional33', password='password3', city="London",
                          email='john3.doe@example.com', phone_number='333333', user_type=UserType.Professional)

        assert list(Professional.filter_professionals_by_city(PROFILE_INFORMATION.get('city')[0])) == [professional]

    def test_filter_by_first_name(self, make_professional):
        professional = make_professional(username='professional11', password='password1', email='john.doe@example.com',
                                         phone_number='111111', user_type=UserType.Professional)
        professional2 = make_professional(username='professional22', password='password2',
                                          email='john2.doe@example.com', phone_number='222222',
                                          user_type=UserType.Professional)
        make_professional(username='professional33', password='password3', first_name="Tal",
                          email='john3.doe@example.com', phone_number='333333', user_type=UserType.Professional)

        assert list(Professional.filter_professionals_by_first_name(USER_INFORMATION.get('first_name')[0])) ==\
               [professional, professional2]

    def test_filter_by_last_name(self, make_professional):
        professional = make_professional(username='professional11', password='password1', email='john.doe@example.com',
                                         phone_number='111111', user_type=UserType.Professional)
        professional2 = make_professional(username='professional22', password='password2',
                                          email='john2.doe@example.com', phone_number='222222',
                                          user_type=UserType.Professional)
        make_professional(username='professional33', password='password3', last_name="Tal",
                          email='john3.doe@example.com', phone_number='333333', user_type=UserType.Professional)

        assert list(Professional.filter_professionals_by_last_name(USER_INFORMATION.get('last_name')[0])) ==\
               [professional, professional2]
