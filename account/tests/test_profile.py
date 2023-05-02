from account.models.profile import Profile
import pytest


PROFILE_TYPE = 'C'
PHONE_NUMBER = '123456789'
COUNTRY = 'USA'
CITY = 'New York'
ADDRESS = '123 Main St'
FIRST_NAME = 'Bob'
LAST_NAME = 'Builder'


@pytest.fixture
def save_profiles(profile1, profile2, profile3):
    profile1.user_id.save()
    profile1.save()
    profile2.user_id.save()
    profile2.save()
    profile3.user_id.save()
    profile3.save()


@pytest.mark.django_db
class TestProfileModel:
    def test_new_profile(self, profile1):
        assert profile1.user_type == PROFILE_TYPE
        assert profile1.phone_number == PHONE_NUMBER
        assert profile1.country == COUNTRY
        assert profile1.city == CITY
        assert profile1.address == ADDRESS

    def test_get_profile(self, profile1):
        profile1.user_id.save()
        profile1.save()
        assert profile1 in Profile.objects.all()

    def test_delete_profile(self, profile1):
        profile1.user_id.save()
        profile1.save()
        profile1.delete()
        assert profile1 not in Profile.objects.all()

    def test_delete_user_deletes_profile(self, profile1):
        profile1.user_id.save()
        profile1.save()
        profile1.user_id.delete()
        assert profile1 not in Profile.objects.all()

    def test_filter_by_city(self, save_profiles, profile1):
        assert list(Profile.filter_by_city(CITY)) == [profile1]

    def test_filter_by_first_name(self, save_profiles, profile3):
        assert list(Profile.filter_by_first_name(FIRST_NAME)) == [profile3]

    def test_filter_by_last_name(self, save_profiles, profile3):
        assert list(Profile.filter_by_last_name(LAST_NAME)) == [profile3]
