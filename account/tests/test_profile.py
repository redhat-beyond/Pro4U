from account.models.profile import Profile
from conftest import USER_INFORMATION
from conftest import PROFILE_INFORMATION
import pytest


@pytest.mark.django_db
class TestProfileModel:
    def test_new_profile(self, make_profile):
        profile = make_profile()
        assert profile.user_type == PROFILE_INFORMATION.get('profile_type')[0]
        assert profile.phone_number == PROFILE_INFORMATION.get('phone_number')[0]
        assert profile.country == PROFILE_INFORMATION.get('country')[0]
        assert profile.city == PROFILE_INFORMATION.get('city')[0]
        assert profile.address == PROFILE_INFORMATION.get('address')[0]

    def test_get_profile(self, make_profile):
        profile = make_profile()
        assert profile in Profile.objects.all()

    def test_delete_profile(self, make_profile):
        profile = make_profile()
        profile.delete()
        assert profile not in Profile.objects.all()

    def test_delete_user_deletes_profile(self, make_profile):
        profile = make_profile()
        profile.user_id.delete()
        assert profile not in Profile.objects.all()

    def test_filter_by_city(self, make_profile):
        profile1 = make_profile(username='client11', password='password1', email='john.doe@example.com',
                                phone_number='111111')
        make_profile(username='client22', password='password2', city='Toronto',
                     email='john2.doe@example.com', phone_number='222222')
        make_profile(username='client33', password='password3', city='London',
                     email='john3.doe@example.com', phone_number='333333')

        assert list(Profile.filter_by_city(PROFILE_INFORMATION.get('city')[0])) == [profile1]

    def test_filter_by_first_name(self, make_profile):
        profile1 = make_profile(username='client11', password='password1', email='john.doe@example.com',
                                phone_number='111111')
        make_profile(username='client22', password='password2', first_name='Tal',
                     email='john2.doe@example.com', phone_number='222222')
        make_profile(username='client33', password='password3', first_name='Tal',
                     email='john3.doe@example.com', phone_number='333333')

        assert list(Profile.filter_by_first_name(USER_INFORMATION.get('first_name')[0])) == [profile1]

    def test_filter_by_last_name(self, make_profile):
        profile1 = make_profile(username='client11', password='password1', email='john.doe@example.com',
                                phone_number='111111')
        make_profile(username='client22', password='password2', last_name='Tal',
                     email='john2.doe@example.com', phone_number='222222')
        make_profile(username='client33', password='password3', last_name='Tal',
                     email='john3.doe@example.com', phone_number='333333')

        assert list(Profile.filter_by_last_name(USER_INFORMATION.get('last_name')[0])) == [profile1]
