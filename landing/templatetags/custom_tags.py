from django import template
from django.core.exceptions import ObjectDoesNotExist

from account.models import professional, client, profile

register = template.Library()


@register.filter
def retrieve_profile_by_user_id(user_id):
    try:
        profile_instance = profile.Profile.objects.get(user_id=user_id)
        return profile_instance
    except ObjectDoesNotExist:
        return None


@register.filter
def retrieve_professional_by_user_id(user_id):
    try:
        professional_instance = professional.Professional.objects.get(profile_id__user_id=user_id)
        return professional_instance
    except ObjectDoesNotExist:
        return None


@register.filter
def retrieve_client_by_user_id(user_id):
    try:
        client_instance = client.Client.objects.get(profile_id__user_id=user_id)
        return client_instance
    except ObjectDoesNotExist:
        return None
