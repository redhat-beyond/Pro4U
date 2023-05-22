from enum import Enum

import pytest
from django.urls import reverse

HOMEPAGE = 'homepage'
USERNAME = 'testuser'
PASSWORD = 'testpassword'
USER_ID = 1


class BaseTemplateObjects(Enum):
    # User menu bar
    SIGN_UP = b'Sign up'
    LOG_IN = b'Log in'
    # Search bar
    SEARCH_DIV_CLASS = b'<div class="input-group">'
    SEARCH = b'Search...'


@pytest.mark.django_db
class TestBaseNavigationBar:
    def test_guest_user_sees_sign_up_and_login_links_but_not_search_bar(self, client):
        response = client.get(reverse(HOMEPAGE))
        # Search bar
        assert BaseTemplateObjects.SEARCH_DIV_CLASS.value not in response.content
        assert BaseTemplateObjects.SEARCH.value not in response.content
        # User menu bar
        assert BaseTemplateObjects.SIGN_UP.value in response.content
        assert BaseTemplateObjects.LOG_IN.value in response.content
