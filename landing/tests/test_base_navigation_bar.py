from enum import Enum

import pytest

HOMEPAGE_VIEW_NAME = 'homepage'
LOGIN_VIEW_NAME = 'login'
USERNAME = 'testusername3'
PASSWORD = 'testpassword3'
USER_ID = 1


class BaseTemplateObjects(Enum):
    # User menu bar
    SIGN_UP = b'Sign up'
    LOG_IN = b'Log in'
    PROFILE = b'Profile'
    LOG_OUT = b'Log out'
    # Search bar
    SEARCH_DIV_CLASS = b'<div class="input-group">'
    SEARCH = b'Search...'
    # Sidebar
    SIDEBAR = b'\'s Sidebar'


@pytest.mark.django_db
class TestBaseNavigationBar:
    def test_guest_user_sees_sign_up_and_login_links_but_not_extended_elements(self, client, get_response):
        response = get_response(HOMEPAGE_VIEW_NAME)
        # Search bar
        assert BaseTemplateObjects.SEARCH_DIV_CLASS.value not in response.content
        assert BaseTemplateObjects.SEARCH.value not in response.content
        # Sidebar
        assert BaseTemplateObjects.SIDEBAR.value not in response.content
        # User menu bar
        assert BaseTemplateObjects.SIGN_UP.value in response.content
        assert BaseTemplateObjects.LOG_IN.value in response.content

    def test_professional_user_sees_relevant_elements_and_links(self, client, get_response, professional):
        self.logged_in_user_sees_relevant_elements_and_links(client, get_response, professional)

    def test_client_user_sees_relevant_elements_and_links(self, client, get_response, demo_client):
        self.logged_in_user_sees_relevant_elements_and_links(client, get_response, demo_client)

    @staticmethod
    def logged_in_user_sees_relevant_elements_and_links(client, get_response, user):
        client.force_login(user.profile_id.user_id)

        response = get_response(HOMEPAGE_VIEW_NAME)
        # Search bar
        assert BaseTemplateObjects.SEARCH_DIV_CLASS.value in response.content
        assert BaseTemplateObjects.SEARCH.value in response.content
        # Sidebar
        user_first_name_sidebar = (user.profile_id.user_id.first_name + BaseTemplateObjects.SIDEBAR.value.decode())
        assert user_first_name_sidebar in response.content.decode()
        # User menu bar
        assert BaseTemplateObjects.PROFILE.value in response.content
        assert BaseTemplateObjects.LOG_OUT.value in response.content
