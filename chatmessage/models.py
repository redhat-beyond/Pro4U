from django.db import models
from django.utils import timezone


class Chatmessage(models.Model):
    message_id = models.IntegerField()
    professional_id = models.CharField(max_length=512)
    client_id = models.CharField(max_length=512)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField()

    class Meta:
        db_table = 'Chatmessage'

    def __str__(self):
        return f"From {self.professional_id} to {self.client_id}: {self.message} [{self.date}]"
