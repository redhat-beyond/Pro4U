from django.db import models
from django.utils import timezone


class SearchHistory(models.Model):
    search_id = models.BigAutoField(primary_key=True)
    professional_id = models.PositiveIntegerField(null=False, blank=False)
    client_id = models.PositiveIntegerField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'SearchHistory'

    @staticmethod
    def get_5_last_professionals_search_by_client(client_id: int):
        lst = SearchHistory.objects.filter(client_id=client_id)
        lst = lst.order_by('-date')[:5]
        lst = lst.values_list('professional_id', flat=True)
        return lst

    def __str__(self):
        return f"{self.client_id} search {self.professional_id} [{self.date}]"
