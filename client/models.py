from django.db import models
import datetime
from user.models import Profile


class Client(models.Model):
    client_id = models.BigAutoField(primary_key=True)
    profile_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    birthday = models.DateField("Birthday", default=datetime.date(2000, 1, 1))

    class Meta:
        db_table = 'client'

    def __str__(self):
        return str(self.client_id)
