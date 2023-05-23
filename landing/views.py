import random

from django.db.models import Avg
from django.shortcuts import render

from landing.context_processors import user_context
from landing.models import TeamMember
from account.models.professional import Professional

MAX_PROFESSIONALS = 48


def homepage(request):
    # TODO: add images for professionals
    db_professionals = Professional.objects.annotate(avg_rating=Avg('review__rating'))
    round_avg_rating(db_professionals)
    professionals = list(db_professionals)
    random.shuffle(professionals)
    context = {
        'professionals': professionals[:MAX_PROFESSIONALS],
    }
    context.update(user_context(request))
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
    context = {
        'team_members': TeamMember.objects.all(),
    }
    context.update(user_context(request))
    return render(request, 'landing/learn-more.html', context=context)
