from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class UserType(models.TextChoices):
    Client = 'C', 'Client'
    Professional = 'P', 'Professional'


class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=UserType.choices, default='C', blank=True)
    phone_number = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=30)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return str(self)

    @staticmethod
    def filter_by_city(city):

        return Profile.objects.filter(city=city) if city else []

    @staticmethod
    def filter_by_first_name(first_name):
        users_ids = User.objects.filter(first_name=first_name).values('id') if first_name else []

        return Profile.objects.filter(Q(user_id__in=users_ids)) if users_ids else []

    @staticmethod
    def filter_by_last_name(last_name):
        users_ids = User.objects.filter(last_name=last_name).values('id') if last_name else []

        return Profile.objects.filter(Q(user_id__in=users_ids)) if users_ids else []
