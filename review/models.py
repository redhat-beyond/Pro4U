from django.db import models
from django.utils import timezone


class Rating(models.TextChoices):
    ONE_STAR = ('1', 'One Star')
    TWO_STARS = ('2', 'Two Stars')
    THREE_STARS = ('3', 'Three Stars')
    FOUR_STARS = ('4', 'Four Stars')
    FIVE_STARS = ('5', 'Five Stars')
    UNSPECIFIED = ('UN', 'Unspecified')


class Review(models.Model):
    rating = models.CharField(max_length=2, choices=Rating.choices, default=Rating.UNSPECIFIED)
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    client_id = models.CharField(max_length=512)
    professional_id = models.CharField(max_length=512)
