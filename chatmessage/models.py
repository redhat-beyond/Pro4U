import uuid
from django.db import models
from django.utils import timezone
#from client.models import Client
#from professional.models import Professional

class Chatmessage(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    #client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField()

    #def __str__(self):
        #return f"From {self.professional_id} to {self.client_id}: {self.message} [{self.date}]"
