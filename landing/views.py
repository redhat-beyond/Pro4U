from django.shortcuts import render

from landing.models import TeamMember


def learn_more(request):
    context = {'team_members': TeamMember.objects.all()}
    return render(request, 'landing/learn-more.html', context=context)
