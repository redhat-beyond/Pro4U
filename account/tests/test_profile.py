from account.models.profile import Profile
from conftest import PROFILE_TYPE
from conftest import PHONE_NUMBER
from conftest import COUNTRY
from conftest import CITY
from conftest import ADDRESS
from conftest import FIRST_NAME
from conftest import LAST_NAME
import pytest


@pytest.mark.django_db
class TestProfileModel:
    def test_new_profile(self, make_profile):
        profile = make_profile()
        assert profile.user_type == PROFILE_TYPE
        assert profile.phone_number == PHONE_NUMBER
        assert profile.country == COUNTRY
        assert profile.city == CITY
        assert profile.address == ADDRESS

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

        assert list(Profile.filter_by_city(CITY)) == [profile1]

    def test_filter_by_first_name(self, make_profile):
        profile1 = make_profile(username='client11', password='password1', email='john.doe@example.com',
                                phone_number='111111')
        make_profile(username='client22', password='password2', first_name='Tal',
                     email='john2.doe@example.com', phone_number='222222')
        make_profile(username='client33', password='password3', first_name='Tal',
                     email='john3.doe@example.com', phone_number='333333')

        assert list(Profile.filter_by_first_name(FIRST_NAME)) == [profile1]

    def test_filter_by_last_name(self, make_profile):
        profile1 = make_profile(username='client11', password='password1', email='john.doe@example.com',
                                phone_number='111111')
        make_profile(username='client22', password='password2', last_name='Tal',
                     email='john2.doe@example.com', phone_number='222222')
        make_profile(username='client33', password='password3', last_name='Tal',
                     email='john3.doe@example.com', phone_number='333333')

        assert list(Profile.filter_by_last_name(LAST_NAME)) == [profile1]
