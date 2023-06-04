from typing import Callable

import pytest

from review.models import Review
from django.template.backends import django

DESCRIPTION = 'Creating a test review'
DAYS = 50
RATING = ['4', '1', '5']


@pytest.mark.django_db
class TestReview:
    def test_get_new_review(self, make_client, professional, create_review):
        review = create_review(make_client(), professional, RATING[0], DESCRIPTION, DAYS)  # Using factory function
        assert review in Review.objects.all()

    def test_get_deleted_review(self, make_client, professional, create_review):
        review = create_review(make_client(), professional, RATING[0], DESCRIPTION, DAYS)  # Using factory function
        Review.objects.filter(id=review.id).delete()
        assert review not in Review.objects.all()

    def test_method_filter_by_professional(self, make_client, professional, create_review):
        review = create_review(make_client(), professional, RATING[0], DESCRIPTION, DAYS)  # Using factory function
        filtered_reviews = Review.filter_by_professional(professional=review.professional)
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

    def test_method_get_professional_avg_rating(self, make_client, professional, create_review):
        # We create new client instance in each tuple in `reviews_data`
        reviews_data = [
            (make_client(username="BBB", first_name="GuyB", phone_number="972541234567"), RATING[0]),
            (make_client(username="AAA", first_name="Guy", phone_number="972541234568"), RATING[1]),
            (make_client(username="CCC", first_name="GuyBe", phone_number="972641214568"), RATING[2]),
        ]

        for i, (client, rating) in enumerate(reviews_data):  # Using factory function within this loop
            create_review(client, professional, rating, DESCRIPTION, DAYS)
            if i == 1:
                assert Review.get_professional_avg_rating(professional=professional) == 2.5  # Average of 2 review

        review_rounded_avg_rating = round(Review.get_professional_avg_rating(professional=professional), 2)
        assert review_rounded_avg_rating == 3.33  # Average of `len(RATING)` reviews

    def test_method_str(self, make_client, professional, create_review: Callable[[str, str, str, str, int], Review]):
        review = str(
            create_review(make_client(), professional, RATING[0], DESCRIPTION, DAYS)
        )  # Using factory function
        assert "Review: #" in review  # Review number
        assert ", by 'Bob Builder'" in review  # Review by
        assert "for 'Bob Builder':" in review  # Review on
        assert "Creating a test review (★★★★)" in review  # Review description
