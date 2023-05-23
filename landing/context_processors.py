from enum import Enum

from django.shortcuts import get_object_or_404

from account.models.client import Client
from account.models.profile import Profile
from account.models.professional import Professional


class UserType(Enum):
    CLIENT = 'C'
    PROFESSIONAL = 'P'


def user_context(request):
    user = request.user
    user_id = None
    if user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=user)

        if profile.user_type == UserType.PROFESSIONAL.value:
            user_id = get_object_or_404(Professional, profile_id=profile)
        elif profile.user_type == UserType.CLIENT.value:
            user_id = get_object_or_404(Client, profile_id=profile)
    return {
        'user_id': user_id,
        'user_type': UserType.__members__,
    }
