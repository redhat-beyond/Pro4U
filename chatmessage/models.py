from django.db import models
from django.utils import timezone
from account.models.professional import Professional
from account.models.client import Client


class SenderType(models.TextChoices):
    Client = 'C'
    Professional = 'P'


class Chatmessage(models.Model):
    sender_type = models.CharField(max_length=1, choices=SenderType.choices, default='C')
    message_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField()

    class Meta:
        db_table = 'Chatmessage'

    def __str__(self):
        return f"From {self.professional_id if self.sender_type == 'P' else self.client_id}"\
               f"to {self.professional_id if self.sender_type == 'P' else self.client_id}: {self.message} [{self.date}]"

    @staticmethod
    def get_all_professional_contacts(professional_id):

        return list({msg.client_id for msg in Chatmessage.objects.filter(professional_id=professional_id)})

    @staticmethod
    def get_all_client_contacts(client_id):

        return list({msg.professional_id for msg in Chatmessage.objects.filter(client_id=client_id)})

    @staticmethod
    def get_chat_between_professional_and_client(professional_id, client_id):

        return Chatmessage.objects.filter(professional_id=professional_id, client_id=client_id)
