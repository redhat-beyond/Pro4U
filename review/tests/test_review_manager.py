from typing import Callable

import pytest
from review.models import Review

TEST_DATA = [
    (1, '3', 'Creating a test review', 0),
    (2, '2', 'Creating a test review', 200),
]


@pytest.mark.django_db
class TestReviewManager:
    def test_sort_review_by_oldest(self, demo_client, demo_client2, professional,
                                   create_review: Callable[[str, str, str, str, int], Review]):
        self.create_reviews(demo_client, demo_client2, professional, create_review)
        # Test sorting sorted_reviews by date (the oldest first)
        sorted_reviews = Review.objects.sort_review_by_oldest()
        self.assert_review(sorted_reviews.first(), rating='2',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating='3',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_newest(self, demo_client, demo_client2, professional,
                                   create_review: Callable[[str, str, str, str, int], Review]):
        self.create_reviews(demo_client, demo_client2, professional, create_review)
        # Test sorting sorted_reviews by date (the newest first)
        sorted_reviews = Review.objects.sort_review_by_newest()
        self.assert_review(sorted_reviews.first(), rating='3',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating='2',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_lowest_rating(self, demo_client, demo_client2, professional,
                                          create_review: Callable[[str, str, str, str, int], Review]):
        self.create_reviews(demo_client, demo_client2, professional, create_review)
        # Test sorting sorted_reviews by rating (the lowest first)
        sorted_reviews = Review.objects.sort_review_by_lowest_rating()
        self.assert_review(sorted_reviews.first(), rating='1',
                           client_full_name='Client3 Client3',
                           professional_full_name='Ido Singer')
        self.assert_review(sorted_reviews.last(), rating='5',
                           client_full_name='Client1 Client1',
                           professional_full_name='Tal Reinfeld')

    def test_sort_review_by_highest_rating(self, demo_client, demo_client2, professional,
                                           create_review: Callable[[str, str, str, str, int], Review]):
        self.create_reviews(demo_client, demo_client2, professional, create_review)
        # Sort the sorted_reviews by highest rating and verify the first one has the highest rating.
        sorted_reviews = Review.objects.sort_review_by_highest_rating()
        self.assert_review(sorted_reviews.first(), rating='5',
                           client_full_name='Client1 Client1',
                           professional_full_name='Tal Reinfeld')
        self.assert_review(sorted_reviews.last(), rating='1',
                           client_full_name='Client3 Client3',
                           professional_full_name='Ido Singer')

    @staticmethod
    def create_reviews(demo_client, demo_client2, professional,
                       create_review: Callable[[str, str, str, str, int], Review]):
        for client_fixture, rating, description, days in TEST_DATA:
            if client_fixture == 1:
                create_review(demo_client, professional, rating, description, days)  # Using factory function
            else:
                create_review(demo_client2, professional, rating, description, days)  # Using factory function

    @staticmethod
    def assert_review(review, rating, client_full_name, professional_full_name):
        client_user = review.client.profile_id.user_id
        professional_user = review.professional.profile_id.user_id
        assert review.rating == rating
        assert f'{client_user.first_name} {client_user.last_name}' == client_full_name
        assert f'{professional_user.first_name} {professional_user.last_name}' == professional_full_name
