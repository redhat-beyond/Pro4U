from django.db import models
from django.contrib.auth.models import User


class UserType(models.TextChoices):
    Client = 'C', 'Client'
    Professional = 'P', 'Professional'


class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=UserType.choices, default='C', blank=True)
    phone_number = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=30)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.title
