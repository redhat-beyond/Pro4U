from django.db import models
from user.models import Profile
# from reservation.model import Appointment, TypeOfJob, Schedule


class Professions(models.TextChoices):
    Plumber = 'PLU', 'Plumber'
    Gardener = 'GAR', 'Gardener'
    Electrician = 'ELE', 'Electrician'
    Tinsmith = 'TIN', 'Tinsmith'
    Painter = 'PAI', 'Painter'
    Locksmith = 'LOC', 'Locksmith'
    Exterminator = 'EXT', 'Exterminator'
    GasTechnician = 'GAT', 'GasTechnician'
    AirConditioningTechnician = 'ACT', 'AirConditioningTechnician'
    RefrigeratorTechnician = 'RET', 'RefrigeratorTechnician'
    Cleaner = 'CLE', 'Cleaner'
    Handyman = 'HAN', 'Handyman'


class Professional(models.Model):
    professional_id = models.BigAutoField(primary_key=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    profession = models.CharField(max_length=3, choices=Professions.choices, blank=True)
    description = models.TextField()
    # schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, default=None)
    # typeOfJob = models.ForeignKey(TypeOfJob, on_delete=models.CASCADE, default=None)
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = 'professional'

    def __str__(self):
        return self.title
