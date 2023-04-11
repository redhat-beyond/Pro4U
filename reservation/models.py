from django.db import models
#from professional.models import Professional
#from client.models import Client

class TypeOfJob(models.Model):
    typeOfJob_ID = models.BigAutoField(primary_key=True)
    #professional_ID = models.ForeignKey(Professional, on_delete=models.CASCADE)
    typeOfName = models.CharField(max_length=120)
    price = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return self.typeOfName

    class Meta:
        db_table = 'TypeOfJob'

class Appointment(models.Model):
    appointment_ID = models.BigAutoField(primary_key=True)
    #professional_ID = models.ForeignKey(Professional, on_delete=models.CASCADE)
    #client_ID = models.ForeignKey(Client, on_delete=models.CASCADE)
    typeOfJob_ID = models.ForeignKey(TypeOfJob, on_delete=models.CASCADE)
    start_appointment = models.DateTimeField()
    end_appointment = models.DateTimeField()
    summary = models.TextField()

    class Meta:
        db_table = 'Appointment'

class Schedule(models.Model):
    schedule_ID = models.BigAutoField(primary_key=True)
    #professional_ID = models.ForeignKey(Professional, on_delete=models.CASCADE)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField()

    class Meta:
        db_table = 'Schedule'








