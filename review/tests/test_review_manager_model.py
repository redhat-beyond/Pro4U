import pytest
from review.models import Review

TEST_DATA = [
    (1, '3', 'Creating a test review', 0),
    (2, '2', 'Creating a test review', 200),
]


@pytest.mark.django_db
class TestReviewManager:
    def test_sort_review_by_oldest(self, make_client, professional, create_review):
        self.create_reviews(make_client, professional, create_review)
        # Test sorting sorted_reviews by date (the oldest first)
        sorted_reviews = Review.objects.sort_review_by_oldest(professional.professional_id)
        self.assert_review(sorted_reviews.first(), rating=Review.Rating.TWO_STARS,
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating='3',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_newest(self, make_client, professional, create_review):
        self.create_reviews(make_client, professional, create_review)
        # Test sorting sorted_reviews by date (the newest first)
        sorted_reviews = Review.objects.sort_review_by_newest(professional.professional_id)
        self.assert_review(sorted_reviews.first(), rating=Review.Rating.THREE_STARS,
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating='2',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_lowest_rating(self, make_client, professional, create_review):
        self.create_reviews(make_client, professional, create_review)
        # Test sorting sorted_reviews by rating (the lowest first)
        sorted_reviews = Review.objects.sort_review_by_lowest_rating(professional.professional_id)
        self.assert_review(sorted_reviews.first(), rating='2',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating=Review.Rating.THREE_STARS,
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_highest_rating(self, make_client, professional, create_review):
        self.create_reviews(make_client, professional, create_review)
        # Sort the sorted_reviews by highest rating and verify the first one has the highest rating.
        sorted_reviews = Review.objects.sort_review_by_highest_rating(professional.professional_id)
        self.assert_review(sorted_reviews.first(), rating='3',
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating=Review.Rating.TWO_STARS,
                           client_full_name='Bob Builder',
                           professional_full_name='Bob Builder')

    @staticmethod
    def create_reviews(make_client, professional, create_review):
        client_user = make_client()
        for client_fixture, rating, description, days in TEST_DATA:
            if client_fixture == 1:
                create_review(client_user, professional, rating, description, days)  # Using factory function
            else:
                create_review(client_user, professional, rating, description, days)  # Using factory function

    @staticmethod
    def assert_review(review, rating, client_full_name, professional_full_name):
        client_user = review.client.profile_id.user_id
        professional_user = review.professional.profile_id.user_id
        assert review.rating == rating
        assert f'{client_user.first_name} {client_user.last_name}' == client_full_name
        assert f'{professional_user.first_name} {professional_user.last_name}' == professional_full_name
