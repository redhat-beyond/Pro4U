from django.contrib.auth import get_user_model
from .models.profile import Profile, UserType
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
class TestProfileModel:

    @pytest.fixture
    def user(self):
        return get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )

    @pytest.fixture
    def saved_profile(self, user):
        profile = Profile.objects.create(
            user_id=user,
            user_type=UserType.Professional,
            phone_number='0000000000',
            country='testcountry',
            city='testcity',
            address='testaddress'
        )
        return profile

    def test_get_profile(self, saved_profile):
        profile = Profile.objects.get(pk=saved_profile.pk)
        assert profile == saved_profile

    def test_delete_profile(self, saved_profile):
        profile = saved_profile
        profile.delete()
        with pytest.raises(Profile.DoesNotExist):
            Profile.objects.get(pk=saved_profile.pk)

    def test_delete_user_deletes_profile(self, saved_profile):
        user = saved_profile.user_id
        user.delete()
        with pytest.raises(Profile.DoesNotExist):
            Profile.objects.get(pk=saved_profile.pk)

    def test_create_profile_with_long_phone_number(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='00000000000000000000',
                country='testcountry',
                city='testcity',
                address='testaddress'
            ).full_clean()

    def test_create_profile_with_blank_phone_number(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='',
                country='testcountry',
                city='testcity',
                address='testaddress'
            ).full_clean()

    def test_create_profile_with_long_country(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='0000000000',
                country='too long country test!',
                city='testcity',
                address='testaddress'
            ).full_clean()

    def test_create_profile_with_blank_country(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='0000000000',
                country='',
                city='testcity',
                address='testaddress'
            ).full_clean()

    def test_create_profile_with_long_city(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='00000000000000000000',
                country='testcountry',
                city='too long city test',
                address='testaddress'
            ).full_clean()

    def test_create_profile_with_blank_city(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='',
                country='testcountry',
                city='',
                address='testaddress'
            ).full_clean()

    def test_create_profile_with_long_address(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='00000000000000000000',
                country='testcountry',
                city='testcity',
                address='too long address test!'
            ).full_clean()

    def test_create_profile_with_blank_phone_number(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type=UserType.Professional,
                phone_number='',
                country='testcountry',
                city='testcity',
                address=''
            ).full_clean()

    def test_create_profile_with_invalid_user_type(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type='invalid user type',
                phone_number='0000000000',
                country='testcountry',
                city='testcity',
                address=''
            ).full_clean()

    def test_create_profile_with_blank_user_type(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                user_type='',
                phone_number='0000000000',
                country='testcountry',
                city='testcity',
                address=''
            ).full_clean()

    def test_create_profile_with_null_user_type(self, user):
        with pytest.raises(ValidationError):
            Profile.objects.create(
                user_id=user,
                phone_number='0000000000',
                country='testcountry',
                city='testcity',
                address=''
            ).full_clean()
