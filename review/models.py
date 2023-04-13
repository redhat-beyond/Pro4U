from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Rating(models.TextChoices):
    ONE_STAR = ('1', 'One Star')
    TWO_STARS = ('2', 'Two Stars')
    THREE_STARS = ('3', 'Three Stars')
    FOUR_STARS = ('4', 'Four Stars')
    FIVE_STARS = ('5', 'Five Stars')
    UNSPECIFIED = ('UN', 'Unspecified')


class Review(models.Model):
    description = models.TextField(blank=True)
    rating = models.CharField(max_length=2, choices=Rating.choices, default=Rating.UNSPECIFIED)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Review"

    def save(self, *args, **kwargs):
        super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})
