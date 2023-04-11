from django.db import models
from django.utils import timezone
# from client.models import Client
# from professional.models import Professional


class SearchHistory(models.Model):
    search_ID = models.BigAutoField(primary_key=True)
    # professional_ID = models.ForeignKey(Professional, on_delete=models.CASCADE)
    # client_ID = models.ForeignKey(Client, on_delete=models.CASCADE)
    professional_ID = models.CharField(max_length=512)
    client_ID = models.CharField(max_length=512)
    date = models.DateTimeField(default=timezone.now)
