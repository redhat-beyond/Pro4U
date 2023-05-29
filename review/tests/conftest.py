from datetime import timedelta
from typing import Callable

import pytest
from django.utils import timezone

from account.models.client import Client
from review.models import Review


@pytest.fixture(scope='function')
def create_review() -> Callable[[str, str, str, str, int], Review]:
    def _review_factory(client: Client, professional: str, rating: str, description: str, days: int) -> Review:
        review = Review.objects.create(
            rating=rating,
            description=description,
            date_posted=timezone.now() - timedelta(days=days),
            client=client,
            professional=professional
        )
        return review

    return _review_factory
