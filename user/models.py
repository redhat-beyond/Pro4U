from django.db import models
from django.contrib.auth.models import User, AbstractUser


# class UserType(models.TextChoices):
#     Client = 'C', 'Client'
#     Professional = 'P', 'Professional'

class Profile(AbstractUser):
    ProfileID = models.BigAutoField(primary_key=True)
    #UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    #UserType = models.CharField(max_length=1, choices=UserType.choices, default='C', blank=True)
    phone_number = models.CharField(max_length=50, unique=True)
    Country = models.CharField(max_length=20)
    City = models.CharField(max_length=20)
    Address = models.CharField(max_length=30)
    last_login = None
    groups = None
    user_permissions = None

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.title