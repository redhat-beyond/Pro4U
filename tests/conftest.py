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


@pytest.fixture
def typeOfJob(professional):
    return TypeOfJob(professional_id=professional, typeOfJob_name=TYPEOFJOB_NAME, price=PRICE)


@pytest.fixture
def persisted_typeOfJob(typeOfJob):
    typeOfJob.professional_id.save()
    typeOfJob.save()
    return typeOfJob


@pytest.fixture
def appointment(typeOfJob, professional, client):
    return Appointment(professional_id=professional, client_id=client, typeOfJob_id=typeOfJob,
                       start_appointment=START_APPOINTMENT, end_appointment=END_APPOINTMENT, summary=SUMMARY)


@pytest.fixture
def persisted_appointment(appointment):
    appointment.typeOfJob_id.save()
    appointment.professional_id.save()
    appointment.client_id.save()
    appointment.save()
    return appointment


@pytest.fixture
def schedule(professional):
    return Schedule(professional_id=professional,
                    start_day=START_DAY,
                    end_day=END_DAY,
                    meeting_time=MEETING_TIME)


@pytest.fixture
def persisted_schedule(schedule):
    schedule.professional_id.save()
    schedule.save()
    return schedule


@pytest.fixture
def chatmessage():
    return Chatmessage(professional_id=professional, client_id=client, message=MESSAGE)


@pytest.fixture
def persisted_chatmessage(chatmessage):
    chatmessage.save()
    return [(chatmessage.message_id), (chatmessage.professional_id),
            (chatmessage.client_id), (chatmessage.date), (chatmessage.message)]


@pytest.fixture
def searchHistory():
    return SearchHistory(professional_id=professional, client_id=client, date=START_DAY)


@pytest.fixture
def persisted_search_history(searchHistory):
    searchHistory.save()
    return [(searchHistory.search_id), (searchHistory.professional_id),
            (searchHistory.client_id), (searchHistory.date)]


@pytest.fixture
def image():
    return Images(professional_id=professional, image=IMAGE_UPLOAD, likes=LIKES)


@pytest.fixture
def persisted_image(image):
    images_object = Images(
        professional_id=professional,
        image=SimpleUploadedFile("test_image1.jpg", b"binary_data"),
        likes=50
        )
    image.save()
    images_object.save()
    return [(image.image, image.likes), (images_object.image, images_object.likes)]


@pytest.fixture
def review():
    now = timezone.now()
    review = Review.objects.create(rating='4', description='Creating a test review...',
                                   date_posted=now - timedelta(days=50),
                                   client_id='client_id', professional_id='professional_id')
    return review


@pytest.fixture
def reviews_manager():
    now = timezone.now()
    review1 = Review.objects.create(rating='5', description='Excellent!', date_posted=now - timedelta(days=3),
                                    client_id='user4', professional_id='pro1')
    review2 = Review.objects.create(rating='4', description='Good', date_posted=now - timedelta(days=1),
                                    client_id='user5', professional_id='pro2')
    review3 = Review.objects.create(rating='3', description='Average', date_posted=now - timedelta(days=2),
                                    client_id='user6', professional_id='pro3')
    return [review1, review2, review3]
