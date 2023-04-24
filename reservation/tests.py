from tests.conftest import *


@pytest.fixture
def persisted_type_of_job_pool(persisted_typeOfJob, professional):
    typeOfJob_object = TypeOfJob(professional_id=professional, typeOfJob_name="Hair cut", price=100)
    typeOfJob_object.professional_id.save()
    typeOfJob_object.save()
    return [(persisted_typeOfJob.typeOfJob_name, persisted_typeOfJob.price),
            (typeOfJob_object.typeOfJob_name, typeOfJob_object.price)]


@pytest.fixture
def persisted_appointment_pool(persisted_appointment, typeOfJob, professional, client2):
    appointment_object = Appointment(professional_id=professional,
                                     client_id=client2,
                                     typeOfJob_id=typeOfJob,
                                     start_appointment=datetime(2023, 4, 20, 12, 0, 0),
                                     end_appointment=datetime(2023, 4, 20, 13, 0, 0),
                                     summary=SUMMARY)
    appointment_object.professional_id.save()
    appointment_object.client_id.save()
    appointment_object.typeOfJob_id.save()
    appointment_object.save()
    return [persisted_appointment.client_id.client_id, appointment_object.client_id.client_id]


@pytest.fixture
def persisted_schedule_pool(persisted_appointment, typeOfJob, persisted_schedule, professional, client2):
    appointment_object = Appointment(professional_id=professional,
                                     client_id=client2,
                                     typeOfJob_id=typeOfJob,
                                     start_appointment=datetime(2023, 4, 17, 13, 0, 0),
                                     end_appointment=datetime(2023, 4, 17, 14, 0, 0),
                                     summary=SUMMARY)

    appointment_object.professional_id.save()
    appointment_object.client_id.save()
    appointment_object.typeOfJob_id.save()
    appointment_object.save()
    return [["10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"],
            ["10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
             "15:00-16:00", "16:00-17:00", "17:00-18:00"]]


@pytest.mark.django_db()
class TestTypeOfJobModel:
    def test_new_typeOfJob(self, typeOfJob, professional):
        assert typeOfJob.professional_id == professional
        assert typeOfJob.typeOfJob_name == TYPEOFJOB_NAME
        assert typeOfJob.price == PRICE

    def test_persist_typeOfJob(self, persisted_typeOfJob):
        assert persisted_typeOfJob in TypeOfJob.objects.all()

    def test_del_typeOfJob(self, persisted_typeOfJob):
        persisted_typeOfJob.delete()
        assert persisted_typeOfJob not in TypeOfJob.objects.all()

    def test_delete_ref_professional(self, persisted_typeOfJob):
        persisted_typeOfJob.professional_id.delete()
        assert persisted_typeOfJob not in TypeOfJob.objects.all()

    def test_get_typeofjobs_name_and_price_by_professional(self, persisted_type_of_job_pool, professional):
        assert persisted_type_of_job_pool == \
               list(TypeOfJob.get_typeofjobs_name_and_price(professional_id=professional))


@pytest.mark.django_db()
class TestAppointmentModel:
    def test_new_appointment(self, appointment, professional, client, typeOfJob):
        assert appointment.professional_id == professional
        assert appointment.client_id == client
        assert appointment.start_appointment == START_APPOINTMENT
        assert appointment.end_appointment == END_APPOINTMENT
        assert appointment.summary == SUMMARY
        assert appointment.typeOfJob_id == typeOfJob

    def test_persist_appointment(self, persisted_appointment):
        assert persisted_appointment in Appointment.objects.all()

    def test_delete_ref_typeOfJob(self, persisted_appointment):
        persisted_appointment.typeOfJob_id.delete()
        assert persisted_appointment not in Appointment.objects.all()

    def test_delete_ref_professional(self, persisted_appointment):
        persisted_appointment.professional_id.delete()
        assert persisted_appointment not in Appointment.objects.all()

    def test_delete_ref_client(self, persisted_appointment):
        persisted_appointment.client_id.delete()
        assert persisted_appointment not in Appointment.objects.all()

    def test_del_appointment(self, persisted_appointment):
        persisted_appointment.delete()
        assert persisted_appointment not in TypeOfJob.objects.all()

    def test_get_clients_by_professional(self, persisted_appointment_pool, professional):
        assert persisted_appointment_pool == list(Appointment.get_clients(professional_id=professional))

    def test_get_client_list_on_certain_day_by_professional_and_date(self, persisted_appointment_pool, professional):
        assert [persisted_appointment_pool[0]] == \
               list(Appointment.get_client_list_on_certain_day(professional_id=professional,
                                                               date=datetime(2023, 4, 17)))


@pytest.mark.django_db()
class TestScheduleModel:
    def test_new_schedule(self, schedule, professional):
        assert schedule.professional_id == professional
        assert schedule.start_day == START_DAY
        assert schedule.end_day == END_DAY
        assert schedule.meeting_time == MEETING_TIME

    def test_persist_schedule(self, persisted_schedule):
        assert persisted_schedule in Schedule.objects.all()

    def test_del_schedule(self, persisted_schedule):
        persisted_schedule.delete()
        assert persisted_schedule not in Schedule.objects.all()

    def test_delete_ref_professional(self, persisted_schedule):
        persisted_schedule.professional_id.delete()
        assert persisted_schedule not in Schedule.objects.all()

    def test_get_possible_meetings_by_professional_and_date(self, persisted_schedule_pool, professional):
        assert persisted_schedule_pool[1] == \
               list(Schedule.get_possible_meetings(professional_id=professional, date=datetime(2023, 4, 17)))

    def test_get_free_meetings_by_professional_and_date(self, persisted_schedule_pool, professional):
        assert persisted_schedule_pool[0] == \
              list(Schedule.get_free_meetings(professional_id=professional, date=datetime(2023, 4, 17)))
