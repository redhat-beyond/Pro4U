import random

from django.db.models import Avg
from django.shortcuts import render

from account.models.professional import Professional

MAX_PROFESSIONALS = 48


def homepage(request):
    # TODO: add images for professionals
    db_professionals = Professional.objects.annotate(avg_rating=Avg('review__rating'))
    # Rounds average rating for each professional
    round_avg_rating(db_professionals)
    # Shuffle professionals randomly
    professionals = list(db_professionals)
    random.shuffle(professionals)
    # Context
    context = {
        'client': None,
        'professionals': professionals[:MAX_PROFESSIONALS]  # Shows only the 'MAX_PROFESSIONALS' first professionals
    }
    return render(request, 'landing/homepage.html', context=context)


def round_avg_rating(professionals):
    """
    f(3.55555555555555)=3.55 -> by rounding. It rounds the avg rating of a professional.
    """
    for professional in professionals:
        if professional.avg_rating is not None:
            professional.avg_rating = round(professional.avg_rating, 1)
        else:
            professional.avg_rating = 'N/A'
