from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from reservation.models import Schedule
from account.models.professional import Professional, Professions
from account.models.profile import Profile, UserType
from reservation.forms import ScheduleForm
from django.contrib.auth.models import User

current_datetime = timezone.now()


class ScheduleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.profile = Profile.objects.create(
            user_id=self.user,
            phone_number='123456789',
            country='USA',
            city='New York',
            address='123 Main St',
            user_type=UserType.Professional
        )
        self.professional = Professional.objects.create(
            profile_id=self.profile,
            profession=Professions.Locksmith,
            description='Test Description')

        self.schedule = Schedule.objects.create(
            professional_id=self.professional,
            start_day=(current_datetime + timedelta(days=5)).replace(hour=10, minute=0,
                                                                     second=0, microsecond=0),
            end_day=(current_datetime + timedelta(days=5)).replace(hour=18, minute=0,
                                                                   second=0, microsecond=0),
            meeting_time=60
        )

    def test_create_schedule(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('schedule_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservation/schedule.html")
        data = {
            'start_day': (current_datetime + timedelta(days=4)).replace(hour=10, minute=0,
                                                                        second=0, microsecond=0),
            'end_day': (current_datetime + timedelta(days=4)).replace(hour=18, minute=0,
                                                                      second=0, microsecond=0),
            'meeting_time': 60
        }

        form = ScheduleForm(data)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse('schedule_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Schedule.objects.filter(professional_id=self.professional).count(), 2)

    def test_create_schedule_invalid_data(self):
        self.client.force_login(self.user)
        data = {
            'start_day': (current_datetime + timedelta(days=4)).replace(hour=10, minute=0,
                                                                        second=0, microsecond=0),
            'end_day': (current_datetime + timedelta(days=4)).replace(hour=9, minute=0,
                                                                      second=0, microsecond=0),
            'meeting_time': 60
        }
        response = self.client.post(reverse('schedule_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Schedule.objects.filter(professional_id=self.professional).count(), 1)
        self.assertRedirects(response, reverse('schedule_new'))

    def test_create_schedule_already_exists(self):
        self.client.force_login(self.user)
        data = {
            'start_day': (current_datetime + timedelta(days=5)).replace(hour=10, minute=0,
                                                                        second=0, microsecond=0),
            'end_day': (current_datetime + timedelta(days=5)).replace(hour=18, minute=0,
                                                                      second=0, microsecond=0),
            'meeting_time': 60
        }
        response = self.client.post(reverse('schedule_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('schedule_new'))
        self.assertEqual(Schedule.objects.filter(professional_id=self.professional).count(), 1)

    def test_schedule_details(self):
        self.client.force_login(self.user)
        url = reverse('schedule_detail', args=[self.schedule.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservation/schedule_details.html")

    def test_schedule_edit(self):
        start_day = (current_datetime + timedelta(days=4)).replace(hour=10, minute=0,
                                                                   second=0, microsecond=0)
        end_day = (current_datetime + timedelta(days=4)).replace(hour=16, minute=0,
                                                                 second=0, microsecond=0)
        self.client.force_login(self.user)
        url = reverse('schedule_edit', args=[self.schedule.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {
            'start_day': start_day,
            'end_day': end_day,
            'meeting_time': 60
        }
        form = ScheduleForm(data)
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.start_day, start_day)
        self.assertEqual(self.schedule.end_day, end_day)
        self.assertEqual(Schedule.objects.filter(professional_id=self.professional).count(), 1)
        self.assertRedirects(response, reverse('schedule_detail', args=[self.schedule.pk]))

    def test_schedule_delete(self):
        self.client.force_login(self.user)
        url = reverse('remove_schedule', args=[self.schedule.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservation/schedule_delete.html")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('calendar'))
        self.assertFalse(Schedule.objects.filter(pk=self.schedule.pk).exists())
        self.assertEqual(Schedule.objects.filter(professional_id=self.professional).count(), 0)
