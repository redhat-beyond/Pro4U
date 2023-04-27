from django.contrib.auth.models import User
from reservation.models import TypeOfJob, Appointment, Schedule
from account.models.profile import Profile
from account.models.professional import Professions, Professional
from account.models.client import Client
from chatmessage.models import Chatmessage
from django.core.files.uploadedfile import SimpleUploadedFile
from proImages.models import Images
from SearchHistory.models import SearchHistory
from review.models import Review
from datetime import datetime, timedelta
from django.utils import timezone
import pytest

BIRTHDAY = datetime(2000, 1, 1)
LAST_LOGIN = datetime.now()


TYPEOFJOB_NAME = "Gel nail polish"
PRICE = 90

START_APPOINTMENT = datetime(2023, 4, 17, 12, 0, 0)
END_APPOINTMENT = datetime(2023, 4, 17, 13, 0, 0)
SUMMARY = ""

START_DAY = datetime(2023, 4, 17, 10, 0, 0)
END_DAY = datetime(2023, 4, 17, 18, 0, 0)
MEETING_TIME = 60

MESSAGE = "message1"

IMAGE_NAME = "test_image.jpg"
IMAGE_UPLOAD = SimpleUploadedFile(IMAGE_NAME, b"binary_data")
LIKES = 100


@pytest.fixture
def user1():
    return User.objects.create_user(username='client1', password='password123', first_name='John', last_name='Doe',
                                    email='john.doe@example.com', last_login=LAST_LOGIN)


@pytest.fixture
def user2():
    return User.objects.create_user(username='client2', password='password456', first_name='Jane',
                                    last_name='Doe', email='jane.doe@example.com', last_login=LAST_LOGIN)


@pytest.fixture
def user3():
    return User.objects.create_user(username='professional1', password='password789', first_name='Bob',
                                    last_name='Builder', email='bob.builder@example.com', last_login=LAST_LOGIN)


@pytest.fixture
def profile1(user1):
    return Profile.objects.create(user_id=user1, phone_number='123456789', country='USA', city='New York',
                                  address='123 Main St', user_type='C')


@pytest.fixture
def profile2(user2):
    return Profile.objects.create(user_id=user2, phone_number='987654321', country='Canada', city='Toronto',
                                  address='456 King St', user_type='C')


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
