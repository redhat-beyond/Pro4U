from typing import Callable

import pytest
from review.models import Review
from django.template.backends import django

DESCRIPTION = 'Creating a test review'
DAYS = 50


@pytest.mark.django_db
class TestReview:
    def test_get_new_review(self, demo_client, professional,
                            create_review: Callable[[str, str, str, str, int], Review]):
        review = create_review(demo_client, professional, '4', DESCRIPTION, DAYS)  # Using factory function
        assert review in Review.objects.all()

    def test_get_deleted_review(self, demo_client, professional,
                                create_review: Callable[[str, str, str, str, int], Review]):
        review = create_review(demo_client, professional, '4', DESCRIPTION, DAYS)  # Using factory function
        Review.objects.filter(id=review.id).delete()
        assert review not in Review.objects.all()

    def test_method_filter_by_professional(self, demo_client, professional,
                                           create_review: Callable[[str, str, str, str, int], Review]):
        review = create_review(demo_client, professional, '4', DESCRIPTION, DAYS)  # Using factory function
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

    def test_method_get_professional_avg_rating(self, demo_client, demo_client2, professional,
                                                create_review: Callable[[str, str, str, str, int], Review]):
        professional_avg_rating = 0
        review = None

        reviews_data1 = [
            (demo_client, '4'),
            (demo_client2, '1'),
        ]
        for client_fixture, rating in reviews_data1:  # Using factory function within this loop
            professional_avg_rating += int(rating)
            review = create_review(client_fixture, professional, rating, DESCRIPTION, DAYS)
        assert Review.get_professional_avg_rating(professional=review.professional) == 2.5  # Average of 2 reviews

        reviews_data2 = [
            (demo_client, '2'),
            (demo_client2, '5'),
        ]
        for client_fixture, rating in reviews_data2:  # Using factory function within this loop
            professional_avg_rating += int(rating)
            review = create_review(client_fixture, professional, rating, DESCRIPTION, DAYS)
        assert Review.get_professional_avg_rating(professional=review.professional) == 3  # Average of 4 reviews

    def test_method_str(self, demo_client, professional, create_review: Callable[[str, str, str, str, int], Review]):
        review = str(
            create_review(demo_client, professional, '4', DESCRIPTION, DAYS)
        )  # Using factory function
        assert "Review: #" in review  # Review number
        assert ", by 'Bob Builder'" in review  # Review by
        assert "for 'Bob Builder':" in review  # Review on
        assert "Creating a test review (★★★★☆ (4/5))" in review  # Review description
