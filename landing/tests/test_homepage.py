from typing import Callable

import pytest
from django.http import HttpResponse
from django.urls import resolve
from pytest_django.asserts import assertTemplateUsed

from account.models.professional import Professional
from landing.views import homepage

HOMEPAGE_VIEW_NAME = 'homepage'


@pytest.mark.django_db
class TestHomepage:
    def test_homepage_url_is_resolved(self, get_url, get_response: Callable[[str], HttpResponse]):
        # Checks that URL endpoint is using view function `homepage`
        assert resolve(get_url(HOMEPAGE_VIEW_NAME)).func == homepage
        assert get_response(HOMEPAGE_VIEW_NAME).status_code == 200

    def test_all_professionals_in_context(self, get_url, get_response: Callable[[str], HttpResponse]):
        # Asserts team members returned in context
        context_professionals = get_response(HOMEPAGE_VIEW_NAME).context['professionals']
        expected_professionals = Professional.objects.all()
        assert len(context_professionals) == len(expected_professionals)
        assert context_professionals != expected_professionals  # context_professionals is in random order

    def test_homepage_GET_success(self, client, get_response: Callable[[str], HttpResponse]):
        assertTemplateUsed(get_response(HOMEPAGE_VIEW_NAME), 'landing/homepage.html')

    def test_homepage_GET_fail(self, client, get_response: Callable[[str], HttpResponse]):
        with pytest.raises(AssertionError):
            assertTemplateUsed(get_response(HOMEPAGE_VIEW_NAME), 'landing/wrong-template.html')
