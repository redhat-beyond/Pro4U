import pytest
from datetime import timedelta
from django.utils import timezone
from review.models import Review
from django.template.backends import django


@pytest.fixture
def review():
    now = timezone.now()
    review = Review.objects.create(rating='4', description='Creating a test review...',
                                   date_posted=now - timedelta(days=50),
                                   client_id='client_id', professional_id='professional_id')
    return review


@pytest.mark.django_db
def test_method_filter_by_professional_id(review):
    filtered_reviews = Review.filter_by_professional_id(professional_id="professional_id")
    filtered_reviews_lst = list(filtered_reviews)

    if isinstance(review, Review):
        assert filtered_reviews_lst == [review]
    elif isinstance(review, django.db.models.query.QuerySet):
        assert filtered_reviews_lst == [*review]
    else:
        error_msg = "review type is neither Review or django.db.models.query.QuerySet"
        with pytest.raises(TypeError, match=error_msg):
            raise TypeError("review type is neither Review or django.db.models.query.QuerySet")

    assert len(filtered_reviews_lst) == 1


@pytest.mark.django_db
def test_method_get_professional_avg_rating(review):
    assert Review.get_professional_avg_rating(professional_id="professional_id") == 4.0


@pytest.mark.django_db
def test_method_str(review):
    assert "Review: #" in str(review)
    assert ", by client_id for professional_id (★★★★☆ (4/5))" in str(review)
