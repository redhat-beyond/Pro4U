from reservation.models import Appointment, TypeOfJob
from datetime import timedelta
from django.utils import timezone
import pytest

current_datetime = timezone.now()
START_APPOINTMENT = (current_datetime + timedelta(days=5)).replace(hour=13, minute=0, second=0, microsecond=0)
END_APPOINTMENT = (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0)
SUMMARY = ""


def save_appointment(appointment: Appointment):
    appointment.professional_id.save()
    appointment.client_id.save()
    appointment.typeOfJob_id.save()
    appointment.save()


@pytest.fixture
def persisted_appointment_pool(make_appointment, client):
    appointment = make_appointment()
    appointment2 = make_appointment(client_id=client,
                                    start_appointment=(current_datetime + timedelta(days=5)).replace(hour=12, minute=0,
                                                                                                     second=0,
                                                                                                     microsecond=0),
                                    end_appointment=(current_datetime + timedelta(days=5)).replace(hour=13, minute=0,
                                                                                                   second=0,
                                                                                                   microsecond=0),
                                    summary="")
    save_appointment(appointment)
    save_appointment(appointment2)
    return [appointment.client_id.client_id, appointment2.client_id.client_id]


@pytest.mark.django_db()
class TestAppointmentModel:
    def test_new_appointment(self, make_appointment, professional, client2, make_typeOfJob):
        typeOfJob = make_typeOfJob(professional_id=professional, typeOfJob_name="Gel nail polish", price=90)
        appointment = make_appointment(typeOfJob_id=typeOfJob)
        assert appointment.professional_id == professional
        assert appointment.client_id == client2
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

    def test_get_clients_by_professional(self, persisted_appointment_pool, professional):
        assert persisted_appointment_pool == list(Appointment.get_clients(professional_id=professional))

    def test_get_client_list_on_certain_day_by_professional_and_date(self, persisted_appointment_pool, professional):
        assert persisted_appointment_pool == \
               list(Appointment.get_client_list_on_certain_day(professional_id=professional,
                                                               date=(current_datetime + timedelta(days=5)).date()))
