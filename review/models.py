from django.db import models
from django.utils import timezone
from django.db.models import Avg


class ReviewManager(models.Manager):
    """
    Class for sorting reviews
    """
    # date
    def sort_review_by_oldest(self):
        # Sorts reviews by dates (oldest first)
        return self.get_queryset().order_by('date_posted')

    def sort_review_by_newest(self):
        # Sorts reviews by dates (newest first)
        return self.get_queryset().order_by('-date_posted')

    # rating
    def sort_review_by_lowest_rating(self):
        # Sorts reviews by rating (lowest first)
        return self.get_queryset().order_by('rating')

    def sort_review_by_highest_rating(self):
        # Sorts reviews by rating (highest first)
        return self.get_queryset().order_by('-rating')


class Review(models.Model):
    class Rating(models.TextChoices):
        ONE_STAR = ('1', '★☆☆☆☆ (1/5)')
        TWO_STARS = ('2', '★★☆☆☆ (2/5)')
        THREE_STARS = ('3', '★★★☆☆ (3/5)')
        FOUR_STARS = ('4', '★★★★☆ (4/5)')
        FIVE_STARS = ('5', '★★★★★ (5/5)')
        UNSPECIFIED = ('UN', 'Unspecified rating')

    rating = models.CharField(max_length=2, choices=Rating.choices, default=Rating.UNSPECIFIED)
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    client_id = models.CharField(max_length=512)
    professional_id = models.CharField(max_length=512)

    objects = ReviewManager()

    @staticmethod
    def filter_by_professional_id(professional_id):
        return Review.objects.filter(professional_id=professional_id)

    @staticmethod
    def get_professional_avg_rating(professional_id):
        filtered_reviews = Review.filter_by_professional_id(professional_id=professional_id)
        return filtered_reviews.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        # get_rating_display() returns the [1] value of an enum.
        id = self.id
        client = self.client_id
        professional = self.professional_id
        rating = self.get_rating_display()
        return f"Review {id} by client {client} for professional {professional} ({rating})"
