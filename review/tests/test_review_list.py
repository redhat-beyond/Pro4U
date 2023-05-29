from enum import Enum

import pytest
from django.urls import reverse

from account.models.professional import Professional
from review.models import Review
from .test_review_model import DESCRIPTION, DAYS, RATING

PROFESSIONAL_ID = 2
REVIEW_LIST_TEMPLATE_NAME = 'review/review_list.html'
SORT_BY_QUERY_PARAM = '?sort_by='


class ReviewListTemplateObjects(Enum):
    # No previous reviews
    NO_REVIEWS = b'No reviews to display.'
    # With previous reviews
    NEWEST = b'Newest'
    OLDEST = b'Oldest'
    HIGHEST = b'Highest'
    LOWEST = b'Lowest'

    WRITE_REVIEW = b'Write a review'  # Client did not review
    EDIT_REVIEW = b'Edit your review'  # Client already have reviewed


@pytest.mark.django_db
class TestReviewList:
    def test_list_is_up(self, client, professional, make_client):
        # demo professional (no previous reviews)
        client.force_login(make_client().profile_id.user_id)
        response = client.get(reverse('reviews', kwargs={'pk': professional.pk}))
        assert response.status_code == 200
        assert REVIEW_LIST_TEMPLATE_NAME in response.templates[0].name

    def test_template_buttons_of_new_professional(self, client, professional, make_client):
        # demo professional (no previous reviews)
        client.force_login(make_client().profile_id.user_id)
        # After creating a new professional, he should not have any reviews
        response = client.get(reverse('reviews', kwargs={'pk': professional.pk}))
        # Page with no reviews check
        assert ReviewListTemplateObjects.NO_REVIEWS.value in response.content
        assert ReviewListTemplateObjects.WRITE_REVIEW.value in response.content

        reviews = response.context['reviews']
        expected_review_count = 0
        assert len(reviews) == expected_review_count

    def test_add_review_to_list(self, client, make_client, professional, create_review):
        client_user = make_client()
        # demo professional (no previous reviews)
        client.force_login(client_user.profile_id.user_id)
        original_review_count = len(
            client.get(
                reverse(
                    'reviews',
                    kwargs={'pk': professional.pk}
                )
            ).context['reviews']
        )
        # After creating a new professional, and adding one review to him, he should have one review
        create_review(client_user, professional, RATING, DESCRIPTION, DAYS)
        response = client.get(reverse('reviews', kwargs={'pk': professional.pk}))
        reviews = response.context['reviews']
        expected_review_count = original_review_count + 1
        assert len(reviews) == expected_review_count

    def test_delete_review_from_list(self, client, make_client):
        # demo professional (no previous reviews)
        client.force_login(make_client().profile_id.user_id)
        original_review_count = len(
            client.get(
                reverse(
                    'reviews',
                    kwargs={'pk': PROFESSIONAL_ID}
                )
            ).context['reviews']
        )
        Review.objects.filter(professional_id=PROFESSIONAL_ID).first().delete()
        updated_review_count = len(
            client.get(
                reverse(
                    'reviews',
                    kwargs={'pk': PROFESSIONAL_ID}
                )
            ).context['reviews']
        )
        expected_review_count = original_review_count - 1
        assert updated_review_count == expected_review_count

    def test_template_buttons_of_existing_professional(self, client, make_client):
        # existing professional (with previous reviews)
        client.force_login(make_client().profile_id.user_id)
        response = client.get(reverse('reviews', kwargs={'pk': PROFESSIONAL_ID}))
        # Page with existing reviews check
        assert ReviewListTemplateObjects.NEWEST.value in response.content
        assert ReviewListTemplateObjects.OLDEST.value in response.content
        assert ReviewListTemplateObjects.HIGHEST.value in response.content
        assert ReviewListTemplateObjects.LOWEST.value in response.content

    def test_template_buttons_are_up_of_existing_professional(self, client, make_client):
        # existing professional (with previous reviews)
        client.force_login(make_client().profile_id.user_id)
        response1 = client.get(reverse('reviews', kwargs={'pk': PROFESSIONAL_ID}) + SORT_BY_QUERY_PARAM + 'newest')
        assert response1.status_code == 200
        assert REVIEW_LIST_TEMPLATE_NAME in response1.templates[0].name
        response2 = client.get(reverse('reviews', kwargs={'pk': PROFESSIONAL_ID}) + SORT_BY_QUERY_PARAM + 'oldest')
        assert response2.status_code == 200
        assert REVIEW_LIST_TEMPLATE_NAME in response2.templates[0].name
        response3 = client.get(reverse('reviews', kwargs={'pk': PROFESSIONAL_ID}) + SORT_BY_QUERY_PARAM + 'highest')
        assert response3.status_code == 200
        assert REVIEW_LIST_TEMPLATE_NAME in response3.templates[0].name
        response4 = client.get(reverse('reviews', kwargs={'pk': PROFESSIONAL_ID}) + SORT_BY_QUERY_PARAM + 'lowest')
        assert response4.status_code == 200
        assert REVIEW_LIST_TEMPLATE_NAME in response4.templates[0].name

    def test_template_review_button_for_client(self, client, make_client, professional, create_review):
        client_user = make_client()
        # existing professional (with previous reviews)
        client.force_login(client_user.profile_id.user_id)
        # After creating a new professional, he should not have any reviews
        response1 = client.get(reverse('reviews', kwargs={'pk': professional.pk}))
        # `client_user` did not review the professional
        assert ReviewListTemplateObjects.WRITE_REVIEW.value in response1.content
        assert ReviewListTemplateObjects.EDIT_REVIEW.value not in response1.content
        # we add review
        professional = Professional.objects.filter(professional_id=PROFESSIONAL_ID).first()
        create_review(client_user, professional, RATING, DESCRIPTION, DAYS)
        # now we check that `client_user` reviewed the professional before
        response2 = client.get(reverse('reviews', kwargs={'pk': PROFESSIONAL_ID}))
        assert ReviewListTemplateObjects.WRITE_REVIEW.value not in response2.content
        assert ReviewListTemplateObjects.EDIT_REVIEW.value in response2.content
