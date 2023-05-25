from django.shortcuts import render, get_object_or_404
from account.models.professional import Professional
from .profile_views import user_profile


def show_profile(request, professional_id):
    professional = get_object_or_404(Professional, pk=professional_id)
    profile = professional.profile_id
    return render(request, 'account/profile.html', {'professional': professional, 'profile': profile})
    # return user_profile(request)
