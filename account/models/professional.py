from django.db import models
from django.db.models import Q
from .profile import Profile


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
    profession = models.CharField(max_length=3, choices=Professions.choices)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'professional'

    def __str__(self):
        return f"Pro id: {self.professional_id}, profession: [{self.profession}], description: {self.description}"

    @staticmethod
    def create_new_professional(username, password, first_name, last_name, email, phone_number,
                                country, city, address, profession, description):
        profile = Profile.create_new_profile(username, password, first_name,
                                             last_name, email, phone_number,
                                             country, city, address)
        professional = Professional(profile_id=profile, profession=profession, description=description)
        professional.save()

        return professional

    @staticmethod
    def delete_professional(professional_id: int):
        profile_id_delete = Professional.objects.filter(professional_id=professional_id).values_list('profile_id',
                                                                                                     flat=True)[0]

        Professional.objects.filter(professional_id=professional_id).delete()
        Profile.delete_profile(profile_id_delete)

    @staticmethod
    def filter_by_professional_id(professional_id):

        return Professional.objects.filter(professional_id=professional_id) if professional_id else []

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

        return Professional.objects.filter(Q(profile_id__in=profile_ids)) if city else []
