from typing import Callable

import pytest
from django.http import HttpResponse
from django.urls import reverse


@pytest.fixture
def get_url() -> Callable[[str], str]:
    def _get_url_factory(view_name: str) -> str:
        return reverse(view_name)

    return _get_url_factory


@pytest.fixture
def get_response(client, get_url) -> Callable[[str], HttpResponse]:
    def _get_response_factory(view_name: str) -> HttpResponse:
        url = get_url(view_name)
        return client.get(url)

    return _get_response_factory
