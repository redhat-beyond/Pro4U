from django.contrib.auth.models import User
from account.models.profile import Profile, UserType
from account.models.professional import Professions, Professional
from account.models.client import Client
from chatmessage.models import Chatmessage, SenderType
from reservation.models import TypeOfJob, Appointment, Schedule
from datetime import timedelta, datetime
from django.utils import timezone
import pytest

current_datetime = timezone.now()

BIRTHDAY = datetime(2000, 1, 1)
LAST_LOGIN = timezone.now()

TYPEOFJOB_NAME = "Hair cut"
PRICE = 100


USER_INFORMATION = {'username': ['testusername', 'testusername2', 'testusername3'],
                    'password': ['testpassword', 'testpassword2', 'testpassword3'],
                    'first_name': ['Bob', 'john'],
                    'last_name': ['Builder'],
                    'email': ['test@test.com', 'test2@test.com', 'test3@test.com'],
                    'last_login': [timezone.now()]}

PROFILE_INFORMATION = {'profile_type': [UserType.Client, UserType.Professional],
                       'phone_number': ['123456789', '987654321', '1212121212'],
                       'country': ['USA'],
                       'city': ['New York'],
                       'address': ['123 Main St']}

PROFESSIONAL_INFORMATION = {'profession': [Professions.Locksmith, Professions.Plumber],
                            'description': ['Test Description']}

CLIENT_INFORMATION = {'birthday': [datetime(2000, 1, 1)]}


@pytest.fixture
def make_user():
    def make(
        username: str = USER_INFORMATION.get('username')[0],
        password: str = USER_INFORMATION.get('password')[0],
        first_name: str = USER_INFORMATION.get('first_name')[0],
        last_name: str = USER_INFORMATION.get('last_name')[0],
        email: str = USER_INFORMATION.get('email')[0],
        last_login: datetime = USER_INFORMATION.get('last_login')[0]
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
        username: str = USER_INFORMATION.get('username')[0],
        password: str = USER_INFORMATION.get('password')[0],
        first_name: str = USER_INFORMATION.get('first_name')[0],
        last_name: str = USER_INFORMATION.get('last_name')[0],
        email: str = USER_INFORMATION.get('email')[0],
        last_login: datetime = USER_INFORMATION.get('last_login')[0],
        phone_number: str = PROFILE_INFORMATION.get('phone_number')[0],
        country: str = PROFILE_INFORMATION.get('country')[0],
        city: str = PROFILE_INFORMATION.get('city')[0],
        address: str = PROFILE_INFORMATION.get('address')[0],
        user_type: UserType = PROFILE_INFORMATION.get('profile_type')[0]
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
        username: str = USER_INFORMATION.get('username')[0],
        password: str = USER_INFORMATION.get('password')[0],
        first_name: str = USER_INFORMATION.get('first_name')[0],
        last_name: str = USER_INFORMATION.get('last_name')[0],
        email: str = USER_INFORMATION.get('email')[0],
        last_login: datetime = USER_INFORMATION.get('last_login')[0],
        phone_number: str = PROFILE_INFORMATION.get('phone_number')[0],
        country: str = PROFILE_INFORMATION.get('country')[0],
        city: str = PROFILE_INFORMATION.get('city')[0],
        address: str = PROFILE_INFORMATION.get('address')[0],
        user_type: UserType = PROFILE_INFORMATION.get('profile_type')[0],
        profession: Professions = PROFESSIONAL_INFORMATION.get('profession')[0],
        description: str = PROFESSIONAL_INFORMATION.get('description')[0],
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
        username: str = USER_INFORMATION.get('username')[0],
        password: str = USER_INFORMATION.get('password')[0],
        first_name: str = USER_INFORMATION.get('first_name')[0],
        last_name: str = USER_INFORMATION.get('last_name')[0],
        email: str = USER_INFORMATION.get('email')[0],
        last_login: datetime = USER_INFORMATION.get('last_login')[0],
        phone_number: str = PROFILE_INFORMATION.get('phone_number')[0],
        country: str = PROFILE_INFORMATION.get('country')[0],
        city: str = PROFILE_INFORMATION.get('city')[0],
        address: str = PROFILE_INFORMATION.get('address')[0],
        user_type: UserType = PROFILE_INFORMATION.get('profile_type')[0],
        birthday: str = CLIENT_INFORMATION.get('birthday')[0],
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
    return make_client(username=USER_INFORMATION.get('username')[1],
                       password=USER_INFORMATION.get('password')[1],
                       email=USER_INFORMATION.get('email')[1],
                       phone_number=PROFILE_INFORMATION.get('phone_number')[1])


@pytest.fixture
def professional(make_professional):
    return make_professional(username=USER_INFORMATION.get('username')[2],
                             password=USER_INFORMATION.get('password')[2],
                             email=USER_INFORMATION.get('email')[2],
                             phone_number=PROFILE_INFORMATION.get('phone_number')[2])


@pytest.fixture
def chatmessage(professional, client):
    return Chatmessage(professional_id=professional,
                       client_id=client, message="message1", sender_type=SenderType.Client)


@pytest.fixture
def make_typeOfJob(professional):
    def make(
        professional_id: Professional = professional,
        typeOfJob_name: str = TYPEOFJOB_NAME,
        price: int = 100,

    ):
        typeOfJob = TypeOfJob.objects.create(professional_id=professional_id, typeOfJob_name=typeOfJob_name,
                                             price=price)
        return typeOfJob

    return make


@pytest.fixture
def make_appointment(professional, client2, make_typeOfJob):
    def make(
        professional_id: Professional = professional,
        client_id: Client = client2,
        typeOfJob_id: TypeOfJob = make_typeOfJob(),
        start_appointment: datetime = (current_datetime + timedelta(days=5)).replace(hour=13, minute=0,
                                                                                     second=0, microsecond=0),
        end_appointment: datetime = (current_datetime + timedelta(days=5)).replace(hour=14, minute=0,
                                                                                   second=0, microsecond=0),
        summary: str = "",
    ):
        appointment = Appointment.objects.create(professional_id=professional_id, client_id=client_id,
                                                 typeOfJob_id=typeOfJob_id,
                                                 start_appointment=start_appointment,
                                                 end_appointment=end_appointment,
                                                 summary=summary)
        return appointment

    return make


@pytest.fixture
def schedule(professional):
    return Schedule(professional_id=professional,
                    start_day=(current_datetime + timedelta(days=5)).replace(hour=10, minute=0,
                                                                             second=0, microsecond=0),
                    end_day=(current_datetime + timedelta(days=5)).replace(hour=18, minute=0,
                                                                           second=0, microsecond=0),
                    meeting_time=60)
