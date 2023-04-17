import pytest
from datetime import timedelta
from django.utils import timezone
from review.models import Review


@pytest.fixture
def review():
    # Checks if the review was created already
    review = Review.objects.filter(client_id='client_id', professional_id='professional_id')
    # Checks if there are at least one object of the same Review and then deletes it
    if len(review) > 0:
            review.delete()
    # Creates and returns a new review object
    now = timezone.now()
    review = Review.objects.create(rating='4', description='Creating a test review...',
                          date_posted=now - timedelta(days=50),
                          client_id='client_id', professional_id='professional_id')
    yield review        # Returns review object
    review.delete()     # TearDown


@pytest.mark.django_db
def test_method_filter_by_professional_id(review):
    filtered_reviews = Review.filter_by_professional_id(professional_id="professional_id")
    filtered_reviews_lst = list(filtered_reviews)

    try:
        if type(review) is Review:
            assert filtered_reviews_lst == [review]
        elif type(review) is django.db.models.query.QuerySet:
            assert filtered_reviews_lst == [*review]
        else:
            raise TypeError
        assert len(filtered_reviews_lst) == 1
    except TypeError:
        print("TypeError: review type is neither Review or django.db.models.query.QuerySet")


@pytest.mark.django_db
def test_method_get_professional_avg_rating(review):
    assert Review.get_professional_avg_rating(professional_id="professional_id") == 4.0


@pytest.mark.django_db
def test_method_str(review):
    assert "Review: #" in str(review)
    assert ", by client_id for professional_id (★★★★☆ (4/5))" in str(review)
