import uuid
from django.db import models
from django.utils import timezone
# from client.models import Client
# from professional.models import Professional


class SearchHistory(models.Model):
	SearchID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	# ProfessionalID = models.ForeignKey(Professional, on_delete=models.CASCADE)
	# ClientID = models.ForeignKey(Client, on_delete=models.CASCADE)
	Date = models.DateTimeField(default=timezone.now)