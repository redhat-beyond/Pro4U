from account.models.profile import Profile
from account.models.professional import Professions, Professional
from account.models.client import Client
from datetime import datetime
import pytest

PROFILE_TYPE = 'C'
PROFESSION = Professions.Locksmith
PHONE_NUMBER = '123456789'
COUNTRY = 'USA'
CITY = 'New York'
ADDRESS = '123 Main St'
DESCRIPTION = 'I'
BIRTHDAY = datetime(2000, 1, 1)


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

    def test_delete_client(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        client.delete()
        assert client not in Client.objects.all()

    def test_delete_user_deletes_client(self, client):
        client.profile_id.user_id.save()
        client.profile_id.save()
        client.save()
        client.profile_id.delete()
        assert client not in Client.objects.all()
