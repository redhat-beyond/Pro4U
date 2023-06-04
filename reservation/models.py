from django.db import models
from datetime import date, datetime, timedelta
from account.models.professional import Professional
from account.models.client import Client
from django.urls import reverse
from django.utils import timezone
import pytz

israel_tz = pytz.timezone('Asia/Jerusalem')
now = timezone.now().astimezone(israel_tz)


class TypeOfJob(models.Model):
    typeOfJob_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    typeOfJob_name = models.CharField(max_length=120)
    price = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return self.typeOfJob_name

    class Meta:
        db_table = 'TypeOfJob'

    @staticmethod
    def get_typeofjobs_by_professional(professional_id: int):
        typeofjobs_by_professional = TypeOfJob.objects.filter(professional_id=professional_id)
        return list(typeofjobs_by_professional)

    @staticmethod
    def get_typeofjobs_name_and_price(professional_id: int):
        typeofjobs_name_and_price_list = TypeOfJob.objects.filter(professional_id=professional_id)\
                                                    .values_list('typeOfJob_name', 'price')
        return typeofjobs_name_and_price_list


class Appointment(models.Model):
    appointment_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    typeOfJob_id = models.ForeignKey(TypeOfJob, on_delete=models.CASCADE)
    start_appointment = models.DateTimeField()
    end_appointment = models.DateTimeField()
    summary = models.TextField(blank=True)

    class Meta:
        db_table = 'Appointment'

    @staticmethod
    def get_appointments_list_after_current_day(profile_id: int, type_of_user: bool):
        appointment_list_after_current_day = []
        if type_of_user is True:
            appointment_list = Appointment.objects.filter(professional_id=profile_id)
        else:
            appointment_list = Appointment.objects.filter(client_id=profile_id)
        for appointment in appointment_list:
            if appointment.start_appointment >= now:
                appointment_list_after_current_day.append(appointment)
        return appointment_list_after_current_day


class Schedule(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField()
    meeting_time = models.PositiveIntegerField(null=False, blank=False)

    @staticmethod
    def get_possible_meetings(professional_id: int, day: int, month: int, year: int):
        professional_schedule_day = Schedule.objects.filter(professional_id=professional_id,
                                                            start_day__day=day,
                                                            start_day__month=month,
                                                            start_day__year=year)

        if not professional_schedule_day:
            return []
        meeting_time = professional_schedule_day[0].meeting_time
        meetings = []
        start_time = datetime.combine(professional_schedule_day[0].start_day.date(),
                                      professional_schedule_day[0].start_day.time())
        end_time = datetime.combine(professional_schedule_day[0].end_day.date(),
                                    professional_schedule_day[0].end_day.time())
        while start_time + timedelta(minutes=meeting_time) <= end_time:
            meetings_str = f"{start_time.time().strftime('%H:%M')}-" \
                           f"{(start_time + timedelta(minutes=meeting_time)).time().strftime('%H:%M')}"
            meetings.append(meetings_str)
            start_time += timedelta(minutes=meeting_time)
        return meetings

    @staticmethod
    def get_free_meetings(professional_id: int, day: int, month: int, year: int):
        free_meetings = []
        meetings = Schedule.get_possible_meetings(professional_id, day, month, year)
        for i, j in enumerate(meetings):
            start_meetings = meetings[i].split("-")[0]
            exists_appointment = Appointment.objects.filter(professional_id=professional_id,
                                                            start_appointment__day=day,
                                                            start_appointment__month=month,
                                                            start_appointment__year=year,
                                                            start_appointment__hour=int(start_meetings.split(":")[0]),
                                                            start_appointment__minute=int(start_meetings.split(":")[1]))
            if len(exists_appointment) == 0:
                free_meetings.append(meetings[i])

        return free_meetings

    @property
    def get_html_url(self):
        url = reverse("schedule_detail", args=(self.schedule_id,))
        start_time = self.start_day.strftime("%H:%M:%S")
        end_time = self.end_day.strftime("%H:%M:%S")
        return f'<a href="{url}"> {start_time} - {end_time} </a>'

    def get_absolute_url(self):
        return reverse("schedule_detail", args=(self.schedule_id,))

    class Meta:
        db_table = 'Schedule'
