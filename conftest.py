from django.contrib.auth.models import User
from account.models.profile import Profile, UserType
from account.models.professional import Professions, Professional
from account.models.client import Client
from chatmessage.models import Chatmessage, SenderType
from datetime import datetime
import pytest


USERNAME = "testusername"
PASSWORD = "testpassword"
FIRST_NAME = 'Bob'
LAST_NAME = 'Builder'
EMAIL = "test@test.com"
LAST_LOGIN = datetime.now()

PROFILE_TYPE = 'C'
PHONE_NUMBER = '123456789'
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
        user = User(
            username=username, password=password, first_name=first_name,
            last_name=last_name, email=email, last_login=last_login
        )
        user.save()
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
        profile = Profile(
            user_id=make_user(username=username, password=password, first_name=first_name,
                              last_name=last_name, email=email, last_login=last_login),
            phone_number=phone_number, country=country, city=city, address=address, user_type=user_type
        )
        profile.save()
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
        professional = Professional(
            profile_id=make_profile(username=username, password=password, first_name=first_name,
                                    last_name=last_name, email=email, last_login=last_login,
                                    phone_number=phone_number, country=country, city=city,
                                    address=address, user_type=user_type),
            profession=profession, description=description
        )
        professional.save()
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
        client = Client(
            profile_id=make_profile(username=username, password=password, first_name=first_name,
                                    last_name=last_name, email=email, last_login=last_login,
                                    phone_number=phone_number, country=country, city=city,
                                    address=address, user_type=user_type), birthday=birthday
        )
        client.save()
        return client

    return make


@pytest.fixture
def client(profile1):
    return Client.objects.create(profile_id=profile1, birthday=BIRTHDAY)


@pytest.fixture
def client2(profile2):
    return Client.objects.create(profile_id=profile2, birthday=BIRTHDAY)


@pytest.fixture
def profile3(user3):
    return Profile.objects.create(user_id=user3, phone_number='5551234', country='UK', city='London',
                                  address='10 Downing St', user_type='P')


@pytest.fixture
def professional(profile3):
    return Professional.objects.create(profile_id=profile3, profession=Professions.Locksmith,
                                       description='I')


@pytest.fixture
def chatmessage(professional, client):
    return Chatmessage(professional_id=professional,
                       client_id=client, message="message1", sender_type=SenderType.Client)
