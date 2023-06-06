import pytest
from django.urls import reverse
from reservation.models import Appointment


@pytest.fixture
def save_schedule(schedule):
    schedule.professional_id.save()
    schedule.save()
    return schedule


@pytest.mark.django_db
class TestMakeAppointment:
    def test_make_appointment_view(self, client, make_client, professional):
        client1 = make_client()
        client.force_login(client1.profile_id.user_id)
        response = client.get(reverse('make_appointment', kwargs={'pk': professional.pk}))
        assert response.status_code == 200
        assert 'reservation/make_appointment.html' in response.templates[0].name

    def test_confirm_appointment_view(self, client, make_client, professional, save_schedule, make_typeOfJob):
        client1 = make_client()
        client.force_login(client1.profile_id.user_id)
        typeOfJob1 = make_typeOfJob()

        data = {
            'service': typeOfJob1.pk  # Include the typeOfJob selected by the user
        }

        response = client.get(reverse('confirm_appointment', kwargs={
            'professional_id': professional.pk,
            'day': save_schedule.start_day.day,
            'month': save_schedule.start_day.month,
            'year': save_schedule.start_day.year,
            'meeting': "10:00-11:00"
        }))
        assert response.status_code == 200
        assert 'reservation/confirm_appointment.html' in response.templates[0].name

        response = client.post(reverse('confirm_appointment', kwargs={
            'professional_id': professional.pk,
            'day': save_schedule.start_day.day,
            'month': save_schedule.start_day.month,
            'year': save_schedule.start_day.year,
            'meeting': '10:00-11:00'
        }), data=data)

        assert response.status_code == 302
        assert response.url == reverse('make_appointment', args=[professional.pk])
        assert Appointment.objects.filter(professional_id=professional).count() == 1
        appointment = Appointment.objects.filter(professional_id=professional).first()
        assert appointment.professional_id.professional_id == professional.pk
        assert appointment.start_appointment.year == save_schedule.start_day.year
        assert appointment.start_appointment.month == save_schedule.start_day.month
        assert appointment.start_appointment.day == save_schedule.start_day.day
        assert appointment.start_appointment.hour == 10
        assert appointment.start_appointment.minute == 0
        assert appointment.end_appointment.year == save_schedule.start_day.year
        assert appointment.end_appointment.month == save_schedule.start_day.month
        assert appointment.end_appointment.day == save_schedule.start_day.day
        assert appointment.end_appointment.hour == 11
        assert appointment.end_appointment.minute == 0
        assert appointment.client_id == client1
