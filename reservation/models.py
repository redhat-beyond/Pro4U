from django.db import models
from datetime import date, datetime, timedelta
from account.models.professional import Professional
from account.models.client import Client


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
    def get_clients(professional_id: int):
        clients_list = Appointment.objects.filter(professional_id=professional_id).values_list('client_id', flat=True)
        return clients_list

    @staticmethod
    def get_client_list_on_certain_day(professional_id: int, date: date):
        client_list_on_certain_day = Appointment.objects.filter(professional_id=professional_id,
                                                                start_appointment__year=date.year,
                                                                start_appointment__month=date.month,
                                                                start_appointment__day=date.day)\
                                                                .values_list('client_id', flat=True)
        return client_list_on_certain_day


class Schedule(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField()
    meeting_time = models.PositiveIntegerField(null=False, blank=False)

    @staticmethod
    def get_possible_meetings(professional_id: int, date: date):
        professional_schedule_day = Schedule.objects.filter(professional_id=professional_id,
                                                            start_day__year=date.year,
                                                            start_day__month=date.month,
                                                            start_day__day=date.day)
        meeting_time = professional_schedule_day[0].meeting_time
        meetings = []
        start_time = datetime.combine(date, professional_schedule_day[0].start_day.time())
        end_time = datetime.combine(date, professional_schedule_day[0].end_day.time())
        while start_time + timedelta(minutes=meeting_time) <= end_time:
            meetings_str = f"{start_time.time().strftime('%H:%M')}-" \
                           f"{(start_time + timedelta(minutes=meeting_time)).time().strftime('%H:%M')}"
            meetings.append(meetings_str)
            start_time += timedelta(minutes=meeting_time)
        return meetings

    @staticmethod
    def get_free_meetings(professional_id: int, date: date):
        free_meetings = []
        meetings = Schedule.get_possible_meetings(professional_id, date)
        for i, j in enumerate(meetings):
            start_meetings = meetings[i].split("-")[0]
            exists_appointment = Appointment.objects.filter(professional_id=professional_id,
                                                            start_appointment__year=date.year,
                                                            start_appointment__month=date.month,
                                                            start_appointment__day=date.day,
                                                            start_appointment__hour=int(start_meetings.split(":")[0]),
                                                            start_appointment__minute=int(start_meetings.split(":")[1]))
            if len(exists_appointment) == 0:
                free_meetings.append(meetings[i])

        return free_meetings

    class Meta:
        db_table = 'Schedule'
