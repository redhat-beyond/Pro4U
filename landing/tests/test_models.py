from typing import Callable

import pytest

from landing.models import TeamMember

TEAM_MEMBER_NAME = 'Guy Beckenstein'


@pytest.mark.django_db
class TestTeamMemberModel:
    def test_add_team_member(self, demo_client, create_team_member: Callable[[str], TeamMember]):
        name = f'{demo_client.profile_id.user_id.first_name} {demo_client.profile_id.user_id.last_name}'
        team_member = create_team_member(name)
        team_member.save()
        assert team_member in TeamMember.objects.all()

    def test_remove_team_member(self, demo_client):
        assert TeamMember.get_member(name=TEAM_MEMBER_NAME).delete() not in TeamMember.objects.all()

    def test_str_method(self, demo_client, create_team_member: Callable[[str], TeamMember]):
        name = f'{demo_client.profile_id.user_id.first_name} {demo_client.profile_id.user_id.last_name}'
        team_member = create_team_member(name)
        assert name == str(team_member)
