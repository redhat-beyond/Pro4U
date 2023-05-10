from typing import Callable

import pytest
from django.http import HttpResponse
from django.urls import resolve
from pytest_django.asserts import assertTemplateUsed

from landing.views import learn_more

LEARN_MORE_VIEW_NAME = 'learn_more'


@pytest.mark.django_db
class TestUrls:
    def test_learn_more_url_is_resolved(self, get_url, get_response: Callable[[str], HttpResponse]):
        # Checks that URL endpoint is using view function `learn_more`
        assert resolve(get_url(LEARN_MORE_VIEW_NAME)).func == learn_more
        assert get_response(LEARN_MORE_VIEW_NAME).status_code == 200

    def test_learn_more_GET_success(self, client, get_response: Callable[[str], HttpResponse]):
        assertTemplateUsed(get_response(LEARN_MORE_VIEW_NAME), 'landing/learn-more.html')

    def test_learn_more_GET_fail(self, client, get_response: Callable[[str], HttpResponse]):
        with pytest.raises(AssertionError):
            assertTemplateUsed(get_response(LEARN_MORE_VIEW_NAME), 'landing/wrong-template.html')
