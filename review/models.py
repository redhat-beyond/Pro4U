from django.db import models
from django.utils import timezone
from django.db.models import Avg

from account.models.client import Client
from account.models.professional import Professional


class ReviewManager(models.Manager):
    """
    Class for sorting reviews
    """
    # date
    def sort_review_by_oldest(self, professional: int):
        # Sorts reviews by dates (the oldest first)
        return self.get_queryset().filter(professional=professional).order_by('date_posted')

    def sort_review_by_newest(self, professional: int):
        # Sorts reviews by dates (the newest first)
        return self.get_queryset().filter(professional=professional).order_by('-date_posted')

    # rating
    def sort_review_by_lowest_rating(self, professional: int):
        # Sorts reviews by rating (the lowest first)
        return self.get_queryset().filter(professional=professional).order_by('rating')

    def sort_review_by_highest_rating(self, professional: int):
        # Sorts reviews by rating (the highest first)
        return self.get_queryset().filter(professional=professional).order_by('-rating')


class Review(models.Model):
    class Rating(models.TextChoices):
        UNSPECIFIED = ('UN', 'Unspecified rating')
        ONE_STAR = ('1', '★')
        TWO_STARS = ('2', '★★')
        THREE_STARS = ('3', '★★★')
        FOUR_STARS = ('4', '★★★★')
        FIVE_STARS = ('5', '★★★★★')

    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    rating = models.CharField(max_length=2, choices=Rating.choices, default=Rating.UNSPECIFIED)
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)

    objects = ReviewManager()

    class Meta:
        db_table = 'Review'

    @staticmethod
    def filter_by_professional(professional):
        return Review.objects.filter(professional=professional)

    @staticmethod
    def get_professional_avg_rating(professional):
        filtered_reviews = Review.filter_by_professional(professional=professional)
        filtered_reviews = filtered_reviews.exclude(rating=Review.Rating.UNSPECIFIED)  # Cannot be calculated in average
        return filtered_reviews.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        client_name = self.client.profile_id.user_id.get_full_name()
        professional_name = self.professional.profile_id.user_id.get_full_name()
        # Modifies review description if the review length is more than 51 letters
        description = self.description
        rating = self.get_rating_display()  # get_rating_display() returns the [1] value of an enum.
        return f"Review: #{self.id}, by '{client_name}' for '{professional_name}': {description} ({rating})"
