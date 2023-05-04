from django.contrib.auth.models import User
from account.models.profile import Profile, UserType
from account.models.professional import Professions, Professional
from account.models.client import Client
from chatmessage.models import Chatmessage, SenderType
from datetime import datetime
from django.utils import timezone
import pytest


USERNAME = "testusername"
USERNAME2 = "testusername2"
USERNAME3 = "testusername3"
PASSWORD = "testpassword"
PASSWORD2 = "testpassword2"
PASSWORD3 = "testpassword3"
FIRST_NAME = 'Bob'
LAST_NAME = 'Builder'
EMAIL = "test@test.com"
EMAIL2 = "test@test2.com"
EMAIL3 = "test@test3.com"
LAST_LOGIN = timezone.now()

PROFILE_TYPE = 'C'
PHONE_NUMBER = '123456789'
PHONE_NUMBER2 = '987654321'
PHONE_NUMBER3 = '1212121212'
COUNTRY = 'USA'
CITY = 'New York'
ADDRESS = '123 Main St'

PROFESSION = Professions.Locksmith
DESCRIPTION = 'Test Description'

BIRTHDAY = datetime(2000, 1, 1)


@pytest.fixture
def make_user():
    def make(
        username: str = USERNAME,
        password: str = PASSWORD,
        first_name: str = FIRST_NAME,
        last_name: str = LAST_NAME,
        email: str = EMAIL,
        last_login: datetime = LAST_LOGIN
    ):
        user = User.objects.create_user(
            username=username, password=password, first_name=first_name,
            last_name=last_name, email=email, last_login=last_login
        )
        return user

    return make


@pytest.fixture
def make_profile(make_user):
    def make(
        username: str = USERNAME,
        password: str = PASSWORD,
        first_name: str = FIRST_NAME,
        last_name: str = LAST_NAME,
        email: str = EMAIL,
        last_login: datetime = LAST_LOGIN,
        phone_number: str = PHONE_NUMBER,
        country: str = COUNTRY,
        city: str = CITY,
        address: str = ADDRESS,
        user_type: UserType = PROFILE_TYPE
    ):
        profile = Profile.objects.create(
            user_id=make_user(username=username, password=password, first_name=first_name,
                              last_name=last_name, email=email, last_login=last_login),
            phone_number=phone_number, country=country, city=city, address=address, user_type=user_type
        )
        return profile

    return make


@pytest.fixture
def make_professional(make_profile):
    def make(
        username: str = USERNAME,
        password: str = PASSWORD,
        first_name: str = FIRST_NAME,
        last_name: str = LAST_NAME,
        email: str = EMAIL,
        last_login: datetime = LAST_LOGIN,
        phone_number: str = PHONE_NUMBER,
        country: str = COUNTRY,
        city: str = CITY,
        address: str = ADDRESS,
        user_type: UserType = PROFILE_TYPE,
        profession: Professions = PROFESSION,
        description: str = DESCRIPTION,
    ):
        professional = Professional.objects.create(
            profile_id=make_profile(username=username, password=password, first_name=first_name,
                                    last_name=last_name, email=email, last_login=last_login,
                                    phone_number=phone_number, country=country, city=city,
                                    address=address, user_type=user_type),
            profession=profession, description=description
        )
        return professional

    return make


@pytest.fixture
def make_client(make_profile):
    def make(
        username: str = USERNAME,
        password: str = PASSWORD,
        first_name: str = FIRST_NAME,
        last_name: str = LAST_NAME,
        email: str = EMAIL,
        last_login: datetime = LAST_LOGIN,
        phone_number: str = PHONE_NUMBER,
        country: str = COUNTRY,
        city: str = CITY,
        address: str = ADDRESS,
        user_type: UserType = PROFILE_TYPE,
        birthday: str = BIRTHDAY,
    ):
        client = Client.objects.create(
            profile_id=make_profile(username=username, password=password, first_name=first_name,
                                    last_name=last_name, email=email, last_login=last_login,
                                    phone_number=phone_number, country=country, city=city,
                                    address=address, user_type=user_type), birthday=birthday
        )
        return client

    return make


@pytest.fixture
def client(make_client):
    return make_client()


@pytest.fixture
def client2(make_client):
    return make_client(username=USERNAME2, password=PASSWORD2, email=EMAIL2, phone_number=PHONE_NUMBER2)


@pytest.fixture
def professional(make_professional):
    return make_professional(username=USERNAME3, password=PASSWORD3, email=EMAIL3, phone_number=PHONE_NUMBER3)


@pytest.fixture
def chatmessage(professional, client):
    return Chatmessage(professional_id=professional,
                       client_id=client, message="message1", sender_type=SenderType.Client)
