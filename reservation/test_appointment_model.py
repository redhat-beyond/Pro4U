from reservation.models import Appointment, TypeOfJob
from datetime import timedelta
from django.utils import timezone
import pytest

current_datetime = timezone.now()
START_APPOINTMENT = (current_datetime + timedelta(days=5)).replace(hour=13, minute=0, second=0, microsecond=0)
END_APPOINTMENT = (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0)
SUMMARY = ""


@pytest.fixture
def persisted_appointment_pool(make_appointment, make_client):
    client = make_client()
    appointment = make_appointment()
    appointment2 = make_appointment(client_id=client,
                                    start_appointment=(current_datetime + timedelta(days=5)).replace(hour=12, minute=0,
                                                                                                     second=0,
                                                                                                     microsecond=0),
                                    end_appointment=(current_datetime + timedelta(days=5)).replace(hour=13, minute=0,
                                                                                                   second=0,
                                                                                                   microsecond=0),
                                    summary="")

    return [appointment, appointment2]


@pytest.mark.django_db()
class TestAppointmentModel:
    def test_new_appointment(self, make_appointment, professional, make_client, make_typeOfJob):
        client = make_client(username='testusername9',
                             password='testpassword9',
                             email='test2@test.com',
                             phone_number="987654379")
        typeOfJob = make_typeOfJob(professional_id=professional, typeOfJob_name="Gel nail polish", price=90)
        appointment = make_appointment(client_id=client, typeOfJob_id=typeOfJob)
        assert appointment.professional_id == professional
        assert appointment.client_id == client
        assert appointment.start_appointment == START_APPOINTMENT
        assert appointment.end_appointment == END_APPOINTMENT
        assert appointment.summary == SUMMARY
        assert appointment.typeOfJob_id == typeOfJob

    def test_persist_appointment(self, make_appointment):
        appointment = make_appointment()
        assert appointment in Appointment.objects.all()

    def test_delete_ref_typeOfJob(self, make_appointment):
        appointment = make_appointment()
        appointment.typeOfJob_id.delete()
        assert appointment not in Appointment.objects.all()

    def test_delete_ref_professional(self, make_appointment):
        appointment = make_appointment()
        appointment.professional_id.delete()
        assert appointment not in Appointment.objects.all()

    def test_delete_ref_client(self, make_appointment):
        appointment = make_appointment()
        appointment.client_id.delete()
        assert appointment not in Appointment.objects.all()

    def test_del_appointment(self, make_appointment):
        appointment = make_appointment()
        appointment.delete()
        assert appointment not in TypeOfJob.objects.all()

    def test_get_appointment_list_after_current_day_by_professional(self, persisted_appointment_pool, professional):
        assert persisted_appointment_pool == \
               list(Appointment.get_appointments_list_after_current_day(profile_id=professional.professional_id,
                                                                        type_of_user=True))

    @pytest.mark.parametrize("appointment", [
        {
            "start_appointment": (current_datetime + timedelta(days=5)).replace(hour=12, minute=0, second=0,
                                                                                microsecond=0),
            "end_appointment": (current_datetime + timedelta(days=5)).replace(hour=13, minute=0, second=0,
                                                                              microsecond=0),
            "summary": ""
        }
    ])
    def test_get_appointment_list_after_current_day_by_client(self, appointment, make_appointment, make_client):
        client = make_client()
        appointment["client_id"] = client
        assert make_appointment(**appointment) == \
               Appointment.get_appointments_list_after_current_day(profile_id=client.client_id,
                                                                   type_of_user=False)[0]
