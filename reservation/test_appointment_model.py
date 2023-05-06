from reservation.models import Appointment, TypeOfJob
from datetime import timedelta
from django.utils import timezone
import pytest

current_datetime = timezone.now()
START_APPOINTMENT = (current_datetime + timedelta(days=5)).replace(hour=12, minute=0, second=0, microsecond=0)
END_APPOINTMENT = (current_datetime + timedelta(days=5)).replace(hour=13, minute=0, second=0, microsecond=0)
SUMMARY = ""


@pytest.fixture
def persisted_appointment(appointment):
    appointment.typeOfJob_id.save()
    appointment.professional_id.save()
    appointment.client_id.save()
    appointment.save()
    return appointment


@pytest.fixture
def persisted_appointment_pool(persisted_appointment, make_appointment):
    appointment = make_appointment()
    appointment.professional_id.save()
    appointment.client_id.save()
    appointment.typeOfJob_id.save()
    appointment.save()
    return [persisted_appointment.client_id.client_id, appointment.client_id.client_id]


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
        assert persisted_appointment_pool == \
               list(Appointment.get_client_list_on_certain_day(professional_id=professional,
                                                               date=(current_datetime + timedelta(days=5)).date()))
