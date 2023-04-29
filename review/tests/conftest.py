# flake8: noqa
from account.tests import client, professional, profile, user  # noqa

from datetime import timedelta

import pytest
from django.utils import timezone

from review.models import Review

RATING = '4'
DESCRIPTION = 'Creating a test review'
DAYS = 50


@pytest.fixture(scope='function')
def create_review(client, professional):
    def _review_factory() -> Review:
        # Review instance
        review = Review.objects.create(
            rating=RATING,
            description=DESCRIPTION,
            date_posted=timezone.now() - timedelta(days=DAYS),
            client=client,
            professional=professional
        )
        return review

    return _review_factory
