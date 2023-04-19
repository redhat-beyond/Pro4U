from django.contrib.auth.models import User
from .models.profile import Profile, UserType
from .models.professional import Professions, Professional
from .models.client import Client
import datetime
import pytest


USERNAME = 'testusername'
PASSWORD = 'testpassword'
FIRST_NAME = 'testfirstname'
LAST_NAME = 'testlastname'
EMAIL = 'test@test.test'
LAST_LOGIN = datetime.datetime.now()

PROFESSIONAL_TYPE = UserType.Professional
CLIENT_TYPE = UserType.Client
PHONE_NUMBER = '1234567890'
COUNTRY = 'testcountry'
CITY = 'testcity'
ADDRESS = 'testaddress'

PROFESSION = Professions.Handyman
DESCRIPTION = 'test description'

BIRTHDAY = datetime.date(2000, 1, 1)

@pytest.fixture
def user():
    user = User.objects.create_user(
        username=USERNAME,
        password=PASSWORD,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        email=EMAIL,
        last_login=LAST_LOGIN
    )
    return user


@pytest.fixture
def profile(user):
    profile = Profile.objects.create(
        user_id=user,
        user_type=PROFESSIONAL_TYPE,
        phone_number=PHONE_NUMBER,
        country=COUNTRY,
        city=CITY,
        address=ADDRESS
    )
    return profile


@pytest.fixture
def professional(profile):
    professional = Profile.objects.create(
        profile_id=profile,
        profile_id_user_type=PROFESSIONAL_TYPE,
        profession=PROFESSION,
        description=DESCRIPTION
    )
    return professional


@pytest.fixture
def client(profile):
    client = Profile.objects.create(
        profile_id=profile,
        profile_id_user_type=CLIENT_TYPE,
        birthday=BIRTHDAY
    )
    return client


@pytest.mark.django_db
class TestProfileModel:
    def test_new_profile(self, profile):
        assert profile.user_type == PROFESSIONAL_TYPE
        assert profile.phone_number == PHONE_NUMBER
        assert profile.country == COUNTRY
        assert profile.city == CITY
        assert profile.address == ADDRESS

    def test_get_profile(self, profile):
        profile.user_id.save()
        profile.save()
        assert profile in Profile.objects.all()

    def test_delete_profile(self, profile):
        profile.user_id.save()
        profile.save()
        profile.delete()
        assert profile not in Profile.objects.all()

    def test_delete_user_deletes_profile(self, profile):
        profile.user_id.save()
        profile.save()
        profile.user_id.delete()
        assert profile not in Profile.objects.all()


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


@pytest.mark.django_db
class TestClientModel:
    def test_new_client(self, client):
        assert client.birthday == BIRTHDAY

    def test_get_client(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        assert client in Client.objects.all()

    def test_delete_professional(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        client.delete()
        assert client not in Client.objects.all()

    def test_delete_user_deletes_professional(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        client.profile_id.delete()
        assert client not in Client.objects.all()
