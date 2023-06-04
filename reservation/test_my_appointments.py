import pytest
from django.urls import reverse
from reservation.models import Appointment


@pytest.mark.django_db
class TestAppointmentList:
    def test_appointment_list_as_professional(self, client, professional, make_appointment):
        appointment = make_appointment()
        client.force_login(professional.profile_id.user_id)
        response = client.get(reverse('my_appointments'))
        assert response.status_code == 200
        assert 'reservation/myAppointments_list.html' in response.templates[0].name
        assert response.context['is_pro'] is True
        my_appointments = response.context['my_appointments']
        assert len(my_appointments) == 1
        assert my_appointments[0] == appointment

    def test_appointment_list_as_client(self, client, make_client, make_appointment):
        client1 = make_client()
        appointment = make_appointment(client_id=client1)  # Pass demo_client argument here
        client.force_login(client1.profile_id.user_id)
        response = client.get(reverse('my_appointments'))
        assert response.status_code == 200
        assert 'reservation/myAppointments_list.html' in response.templates[0].name
        assert response.context['is_pro'] is False
        my_appointments = response.context['my_appointments']
        assert len(my_appointments) == 1
        assert my_appointments[0] == appointment


@pytest.mark.django_db
class TestAppointmentDelete:
    def test_appointment_delete_by_professional(self, professional, make_appointment, client):
        appointment = make_appointment()
        client.force_login(professional.profile_id.user_id)
        response = client.post(reverse('appointment_delete', kwargs={'pk': appointment.pk}))
        assert response.status_code == 302
        assert response.url == reverse('my_appointments')
        assert Appointment.objects.filter(professional_id=professional).count() == 0

    def test_appointment_delete_by_client(self, make_client, make_appointment, client):
        client1 = make_client()
        appointment = make_appointment(client_id=client1)
        client.force_login(client1.profile_id.user_id)
        response = client.post(reverse('appointment_delete', kwargs={'pk': appointment.pk}))
        assert response.status_code == 302
        assert response.url == reverse('my_appointments')
        assert Appointment.objects.filter(client_id=client1).count() == 0
