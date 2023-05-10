from typing import Callable

import pytest
from django.http import HttpResponse
from django.urls import reverse

from landing.models import TeamMember


@pytest.fixture(scope='function')
def create_team_member(demo_client) -> Callable[[str], TeamMember]:
    def _team_member_factory(name: str) -> TeamMember:
        name_without_whitespaces = ''.join(name.split())
        team_member = TeamMember(
            name=name,
            img=f'/img/{name_without_whitespaces}.jpg',
            alt=name_without_whitespaces,
        )
        return team_member
    return _team_member_factory


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
