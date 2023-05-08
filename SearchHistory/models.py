from django.db import models
from django.utils import timezone
from account.models.professional import Professional
from account.models.client import Client
from django.db.models import Max


class SearchHistory(models.Model):
    search_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'SearchHistory'

    def __str__(self):
        return f"{self.client_id} search {self.professional_id} [{self.date}]"

    @staticmethod
    def get_last_professionals_search_by_client(client_id, expected_result=5):
        lst = SearchHistory.objects.filter(client_id=client_id)
        lst = lst.values('professional_id').annotate(max_date=Max('date'))
        lst = lst.order_by('-max_date')[:expected_result]
        lst = [row['professional_id'] for row in lst]
        return list(lst)
