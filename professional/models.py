from django.db import models
from user.models import Profile
from django.db.models import Q


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
    profile_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    profession = models.CharField(max_length=3, choices=Professions.choices, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'professional'

    def __str__(self):
        return str(self)

    @staticmethod
    def filter_by_profession(profession):

        return Professional.objects.filter(profession=profession) if profession else []

    @staticmethod
    def filter_professionals_by_first_name(first_name):
        profile_ids = Profile.filter_by_first_name(first_name).values('profile_id') if first_name else []

        return Professional.objects.filter(Q(profile_id__in=profile_ids)) if profile_ids else []

    @staticmethod
    def filter_professionals_by_last_name(last_name):
        profile_ids = Profile.filter_by_last_name(last_name).values('profile_id') if last_name else []

        return Professional.objects.filter(Q(profile_id__in=profile_ids)) if profile_ids else []

    @staticmethod
    def filter_professionals_by_city(city):
        profile_ids = Profile.filter_by_city(city).values('profile_id') if city else []

        return Profile.objects.filter(Q(profile_id__in=profile_ids)) if city else []
