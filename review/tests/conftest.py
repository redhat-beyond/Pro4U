from datetime import timedelta
from typing import Callable

import pytest
from django.utils import timezone

from review.models import Review


@pytest.fixture(scope='function')
def create_review() -> Callable[[str, str, str, str, int], Review]:
    def _review_factory(client: str, professional: str, rating: str, description: str, days: int) -> Review:
        # Review function instance, currently without parameters. The main idea is that if `create_review` fixture
        # is called in a test, we can call the factory with `create_review(X1,...,Xn)`, thus the parameters (X1,...Xn)
        # will allow non hard-coded usage of `create_review` fixture i.e. we can add parameters to tests using fixtures.
        review = Review.objects.create(
            rating=rating,
            description=description,
            date_posted=timezone.now() - timedelta(days=days),
            client=client,
            professional=professional
        )
        return review

    return _review_factory
