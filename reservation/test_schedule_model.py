from reservation.models import Schedule, Appointment
from datetime import timedelta
from django.utils import timezone
import pytest

current_datetime = timezone.now()
START_DAY = (current_datetime + timedelta(days=5)).replace(hour=10, minute=0, second=0, microsecond=0)
END_DAY = (current_datetime + timedelta(days=5)).replace(hour=18, minute=0, second=0, microsecond=0)
MEETING_TIME = 60


@pytest.fixture
def persisted_schedule(schedule):
    schedule.professional_id.save()
    schedule.save()
    return schedule


@pytest.fixture
def persisted_schedule_pool(appointment, persisted_schedule, make_appointment):
    appointment2 = make_appointment()
    appointment.typeOfJob_id.save()
    appointment.professional_id.save()
    appointment.client_id.save()
    appointment.save()
    appointment2.professional_id.save()
    appointment2.client_id.save()
    appointment2.typeOfJob_id.save()
    appointment2.save()
    return [["10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"],
            ["10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
             "15:00-16:00", "16:00-17:00", "17:00-18:00"]]


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
               list(Schedule.get_possible_meetings(professional_id=professional, date=(current_datetime +
                                                                                       timedelta(days=5)).date()))

    def test_get_free_meetings_by_professional_and_date(self, persisted_schedule_pool, professional):
        assert persisted_schedule_pool[0] == \
              list(Schedule.get_free_meetings(professional_id=professional, date=(current_datetime +
                                                                                  timedelta(days=5)).date()))
