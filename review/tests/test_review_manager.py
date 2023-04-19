import pytest
from datetime import timedelta
from django.utils import timezone
from review.models import Review


@pytest.fixture
def reviews():
    now = timezone.now()
    review1 = Review.objects.create(rating='5', description='Excellent!', date_posted=now - timedelta(days=3),
                                    client_id='user4', professional_id='pro1')
    review2 = Review.objects.create(rating='4', description='Good', date_posted=now - timedelta(days=1),
                                    client_id='user5', professional_id='pro2')
    review3 = Review.objects.create(rating='3', description='Average', date_posted=now - timedelta(days=2),
                                    client_id='user6', professional_id='pro3')
    return [review1, review2, review3]


@pytest.mark.django_db
def test_sort_review_by_oldest(reviews):
    # Test sorting reviews by date (the oldest first)
    reviews = Review.objects.sort_review_by_oldest()
    assert_review(reviews.first(), rating='4', client_id='user2', professional_id='pro2')
    assert_review(reviews.last(), rating='4', client_id='user5', professional_id='pro2')


@pytest.mark.django_db
def test_sort_review_by_newest(reviews):
    # Test sorting reviews by date (the newest first)
    reviews = Review.objects.sort_review_by_newest()
    assert_review(reviews.first(), rating='4', client_id='user5', professional_id='pro2')
    assert_review(reviews.last(), rating='4', client_id='user2', professional_id='pro2')


@pytest.mark.django_db
def test_sort_review_by_lowest_rating(reviews):
    # Test sorting reviews by rating (the lowest first)
    reviews = Review.objects.sort_review_by_lowest_rating()
    assert_review(reviews.first(), rating='1', client_id='user3', professional_id='pro2')
    assert_review(reviews.last(), rating='5', client_id='user1', professional_id='pro1')


@pytest.mark.django_db
def test_sort_review_by_highest_rating(reviews):
    # Sort the reviews by highest rating and verify the first one has the highest rating.
    reviews = Review.objects.sort_review_by_highest_rating()
    assert_review(reviews.first(), rating='5', client_id='user1', professional_id='pro1')
    assert_review(reviews.last(), rating='1', client_id='user3', professional_id='pro2')


def assert_review(review, rating, client_id, professional_id):
    assert review.rating == rating
    assert review.client_id == client_id
    assert review.professional_id == professional_id
