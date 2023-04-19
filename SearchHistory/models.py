from django.db import models
from django.utils import timezone


class SearchHistory(models.Model):
    search_ID = models.BigAutoField(primary_key=True)
    professional_ID = models.PositiveIntegerField(null=False, blank=False)
    client_ID = models.PositiveIntegerField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)


class Meta:
    db_table = 'SearchHistory'


def __str__(self):
    return f"{self.client_ID} search {self.professional_ID} [{self.date}]"


@staticmethod
def get_last_professionals_search_by_client(client_ID: int):
    client_professionals_search = SearchHistory.objects.filter(client_ID=client_ID)
    return client_professionals_search.get_queryset().order_by('-date')


@staticmethod
def get_clients_that_search_professional(professional_ID: int):
    return SearchHistory.objects.filter(professional_ID=professional_ID).values_list('client_id', flat=True)
