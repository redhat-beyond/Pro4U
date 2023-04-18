import pytest
from reservation.models import TypeOfJob, Appointment, Schedule
from datetime import datetime

PROFESSIONAL_ID = 4
TYPEOFJOB_NAME = "Gel nail polish"
PRICE = 90

CLIENT_ID = 3
START_APPOINTMENT = datetime(2023, 4, 17, 12, 0, 0)
END_APPOINTMENT = datetime(2023, 4, 17, 13, 0, 0)
SUMMARY = ""

START_DAY = datetime(2023, 4, 17, 10, 0, 0)
END_DAY = datetime(2023, 4, 17, 18, 0, 0)
MEETING_TIME = 60


@pytest.fixture
def typeOfJob():
    return TypeOfJob(professional_id=PROFESSIONAL_ID, typeOfJob_name=TYPEOFJOB_NAME, price=PRICE)


@pytest.fixture
def persisted_type_of_job_pool(typeOfJob):
    typeOfJob_object = TypeOfJob(professional_id=PROFESSIONAL_ID, typeOfJob_name="Hair cut", price=100)
    typeOfJob.save()
    typeOfJob_object.save()
    return [(typeOfJob.typeOfJob_name, typeOfJob.price), (typeOfJob_object.typeOfJob_name, typeOfJob_object.price)]


@pytest.fixture
def appointment(typeOfJob):
    return Appointment(professional_id=PROFESSIONAL_ID, client_id=CLIENT_ID, typeOfJob_id=typeOfJob,
                       start_appointment=START_APPOINTMENT, end_appointment=END_APPOINTMENT, summary=SUMMARY)


@pytest.fixture
def persisted_appointment(appointment):
    appointment.typeOfJob_id.save()
    appointment.save()
    return appointment


@pytest.fixture
def persisted_appointment_pool(persisted_appointment):
    typeOfJob_object = TypeOfJob(professional_id=PROFESSIONAL_ID, typeOfJob_name="Hair cut", price=100)
    appointment_object = Appointment(professional_id=PROFESSIONAL_ID,
                                     client_id=10,
                                     typeOfJob_id=typeOfJob_object,
                                     start_appointment=datetime(2023, 4, 20, 12, 0, 0),
                                     end_appointment=datetime(2023, 4, 20, 13, 0, 0),
                                     summary=SUMMARY)
    typeOfJob_object.save()
    appointment_object.save()
    return [persisted_appointment.client_id, appointment_object.client_id]


@pytest.fixture
def schedule():
    return Schedule(professional_id=PROFESSIONAL_ID,
                    start_day=START_DAY,
                    end_day=END_DAY,
                    meeting_time=MEETING_TIME)


@pytest.fixture
def persisted_schedule_pool(persisted_appointment, schedule):
    typeOfJob_object = TypeOfJob(professional_id=PROFESSIONAL_ID, typeOfJob_name="Hair cut", price=100)
    appointment_object1 = Appointment(professional_id=PROFESSIONAL_ID,
                                      client_id=10,
                                      typeOfJob_id=typeOfJob_object,
                                      start_appointment=datetime(2023, 4, 17, 13, 0, 0),
                                      end_appointment=datetime(2023, 4, 17, 14, 0, 0),
                                      summary=SUMMARY)

    typeOfJob_object.save()
    appointment_object1.save()
    persisted_appointment.save()
    schedule.save()
    return [["10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"],
            ["10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
             "15:00-16:00", "16:00-17:00", "17:00-18:00"]]


@pytest.mark.django_db()
class TestTypeOfJobModel:
    def test_new_typeOfJob(self, typeOfJob):
        assert typeOfJob.professional_id == PROFESSIONAL_ID
        assert typeOfJob.typeOfJob_name == TYPEOFJOB_NAME
        assert typeOfJob.price == PRICE

    def test_persist_typeOfJob(self, typeOfJob):
        typeOfJob.save()
        assert typeOfJob in TypeOfJob.objects.all()

    def test_del_typeOfJob(self, typeOfJob):
        typeOfJob.save()
        typeOfJob.delete()
        assert typeOfJob not in TypeOfJob.objects.all()

    def test_get_typeofjobs_name_and_price_by_professional(self, persisted_type_of_job_pool):
        assert persisted_type_of_job_pool == \
               list(TypeOfJob.get_typeofjobs_name_and_price(professional_id=PROFESSIONAL_ID))


@pytest.mark.django_db()
class TestAppointmentModel:
    def test_new_appointment(self, appointment):
        assert appointment.professional_id == PROFESSIONAL_ID
        assert appointment.client_id == CLIENT_ID
        assert appointment.start_appointment == START_APPOINTMENT
        assert appointment.end_appointment == END_APPOINTMENT
        assert appointment.summary == SUMMARY
        assert appointment.typeOfJob_id.professional_id == PROFESSIONAL_ID
        assert appointment.typeOfJob_id.typeOfJob_name == TYPEOFJOB_NAME
        assert appointment.typeOfJob_id.price == PRICE

    def test_persist_appointment(self, appointment):
        appointment.typeOfJob_id.save()
        appointment.save()
        assert appointment in Appointment.objects.all()

    def test_delete_ref_typeOfJob(self, persisted_appointment):
        persisted_appointment.typeOfJob_id.delete()
        assert persisted_appointment not in Appointment.objects.all()

    def test_del_appointment(self, persisted_appointment):
        persisted_appointment.delete()
        assert persisted_appointment not in TypeOfJob.objects.all()

    def test_get_clients_by_professional(self, persisted_appointment_pool):
        assert persisted_appointment_pool == list(Appointment.get_clients(professional_id=PROFESSIONAL_ID))

    def test_get_client_list_on_certain_day_by_professional_and_date(self, persisted_appointment_pool):
        assert [persisted_appointment_pool[0]] == \
               list(Appointment.get_client_list_on_certain_day(professional_id=PROFESSIONAL_ID,
                                                               date=datetime(2023, 4, 17)))


@pytest.mark.django_db()
class TestScheduleModel:
    def test_new_schedule(self, schedule):
        assert schedule.professional_id == PROFESSIONAL_ID
        assert schedule.start_day == START_DAY
        assert schedule.end_day == END_DAY
        assert schedule.meeting_time == MEETING_TIME

    def test_persist_schedule(self, schedule):
        schedule.save()
        assert schedule in Schedule.objects.all()

    def test_del_schedule(self, schedule):
        schedule.save()
        schedule.delete()
        assert schedule not in Schedule.objects.all()

    def test_get_possible_meetings_by_professional_and_date(self, persisted_schedule_pool):
        assert persisted_schedule_pool[1] == \
               list(Schedule.get_possible_meetings(professional_id=PROFESSIONAL_ID, date=datetime(2023, 4, 17)))

    def test_get_free_meetings_by_professional_and_date(self, persisted_schedule_pool):
        assert persisted_schedule_pool[0] == \
               list(Schedule.get_free_meetings(professional_id=PROFESSIONAL_ID, date=datetime(2023, 4, 17)))
