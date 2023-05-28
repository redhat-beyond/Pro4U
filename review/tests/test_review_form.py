from enum import Enum

import pytest
from django.urls import reverse

from review.tests.test_review_model import RATING, DESCRIPTION, DAYS


class ReviewFormTemplateObjects(Enum):
    DESCRIPTION_HEADER = b'Share more about your experience'
    DESCRIPTION_PLACEHOLDER = b'Share details of your own experience with this professional'
    BUTTON1 = b'Cancel'
    BUTTON2 = b'Post'


@pytest.mark.django_db
class TestForms:
    def test_GET_request_create_form_success(self, client, make_client, professional):
        client.force_login(make_client().profile_id.user_id)
        url = reverse('review-create', kwargs={'pk': professional.pk})
        response = client.get(url)
        self.assert_review_form(response, expected_status_code=200)
        # Test the review form template objects existence
        assert ReviewFormTemplateObjects.DESCRIPTION_HEADER.value in response.content
        assert ReviewFormTemplateObjects.DESCRIPTION_PLACEHOLDER.value in response.content
        assert ReviewFormTemplateObjects.BUTTON1.value in response.content
        assert ReviewFormTemplateObjects.BUTTON2.value in response.content

    def test_GET_request_create_form_fail(self, client, make_client, professional, create_review):
        client_user = make_client()
        # `make_client` with review to `professional`. He is redirected to a different URL
        client.force_login(client_user.profile_id.user_id)
        create_review(client_user, professional, RATING, DESCRIPTION, DAYS)
        url = reverse('review-create', kwargs={'pk': professional.pk})
        response = client.get(url)
        self.assert_review_form(response, expected_status_code=302)

    def test_review_update_form_success(self, client, make_client, professional, create_review):
        client_user = make_client()
        client.force_login(client_user.profile_id.user_id)
        create_review(client_user, professional, RATING, DESCRIPTION, DAYS)
        url = reverse('review-update', kwargs={'pk': professional.pk})
        response = client.get(url)
        self.assert_review_form(response, expected_status_code=200)

    def test_review_update_form_fail(self, client, make_client, professional, create_review):
        # `make_client` must review `professional` before entering update page
        client.force_login(make_client().profile_id.user_id)
        url = reverse('review-update', kwargs={'pk': professional.pk})
        response = client.get(url)
        self.assert_review_form(response, expected_status_code=404)

    @staticmethod
    def assert_review_form(response, expected_status_code):
        assert response.status_code == expected_status_code
        if response.status_code == 404:
            assert response.templates[0].name is None
        elif response.templates:  # failed GET requests don't have `response.templates`
            assert 'review/review_form.html' in response.templates[0].name
