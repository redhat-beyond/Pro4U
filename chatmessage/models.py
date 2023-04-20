from django.db import models
from django.utils import timezone


class Chatmessage(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    professional_id = models.CharField(max_length=512)
    client_id = models.CharField(max_length=512)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField()

    class Meta:
        db_table = 'Chatmessage'

    def __str__(self):
        return f"From {self.professional_id} to {self.client_id}: {self.message} [{self.date}]"

    @staticmethod
    def get_all_professional_contacts(professional_id):

        return list({msg.client_id for msg in Chatmessage.objects.filter(professional_id=professional_id)})

    @staticmethod
    def get_all_client_contacts(client_id):

        return list({msg.professional_id for msg in Chatmessage.objects.filter(client_id=client_id)})

    @staticmethod
    def get_chat_between_professional_and_client(professional_id, client_id):

        return Chatmessage.objects.filter(professional_id=professional_id, client_id=client_id)
