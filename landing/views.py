import random

from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from account.models.client import Client
from account.models.profile import Profile
from landing.models import TeamMember
from account.models.professional import Professional

MAX_PROFESSIONALS = 48


def homepage(request):
    user = request.user
    user_id = None

    if user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=user)

        if profile.user_type == 'C':
            user_id = get_object_or_404(Client, profile_id=profile)
        elif profile.user_type == 'P':
            user_id = get_object_or_404(Professional, profile_id=profile)

    # TODO: add images for professionals
    db_professionals = Professional.objects.annotate(avg_rating=Avg('review__rating'))
    # Rounds average rating for each professional
    round_avg_rating(db_professionals)
    # Shuffle professionals randomly
    professionals = list(db_professionals)
    random.shuffle(professionals)
    # Context
    context = {
        'user_id': user_id,
        'professionals': professionals[:MAX_PROFESSIONALS],  # Shows only the 'MAX_PROFESSIONALS' first professionals
    }
    return render(request, 'landing/homepage.html', context=context)


def round_avg_rating(professionals):
    """
    f(3.67124)=3.7 -> by rounding. It rounds the avg rating of a professional.
    """
    for professional in professionals:
        if professional.avg_rating is not None:
            professional.avg_rating = round(professional.avg_rating, 1)
        else:
            professional.avg_rating = 'N/A'


def learn_more(request):
    context = {'team_members': TeamMember.objects.all()}
    return render(request, 'landing/learn-more.html', context=context)
