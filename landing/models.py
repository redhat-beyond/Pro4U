from django.db import models
from django.db.models import QuerySet


class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=30)
    img = models.CharField(max_length=50)
    alt = models.CharField(max_length=30)

    class Meta:
        db_table = 'TeamMember'

    @staticmethod
    def get_member(name: str) -> QuerySet:
        return TeamMember.objects.filter(name=name)

    def __str__(self):
        return self.name
