from django.shortcuts import render
from account.models.professional import Professional
from account.models.client import Client
from django.db.models import Q
from SearchHistory.models import SearchHistory


def search(request, user_id):

    professionals = Professional.objects.all()
    last_searches = SearchHistory.get_last_professionals_search_by_client(client_id=user_id)

    context = {
        'professionals': professionals,
        'last_searches': last_searches,
    }

    if request.method == 'GET':
        return render(request, 'html/search.html', context=context)

    elif request.method == 'POST':
        if request.POST.get("opened", "") == '0':

            professionals = Professional.objects.all()

            professional_id = request.POST.get("professional_id", "")
            profession = request.POST.get("profession", "")
            first_name = request.POST.get("first_name", "")
            last_name = request.POST.get("last_name", "")
            city = request.POST.get("city", "")

            professionals = professionals.filter(
                Q(professional_id=professional_id) if professional_id else Q(),
                Q(profession=profession) if profession else Q(),
                Q(profile_id__user_id__first_name=first_name) if first_name else Q(),
                Q(profile_id__user_id__last_name=last_name) if last_name else Q(),
                Q(profile_id__city=city) if city else Q()
            )

            if not professionals.exists():
                professionals = []

        context = {
            'professionals': professionals,
            'last_searches': last_searches,
        }

        if request.POST.get("opened", "") == '1':
            professional_id = request.POST.get("search_results_professional_id", "")
            professional = Professional.filter_by_professional_id(professional_id)
            client = Client.filter_by_client_id(user_id)
            SearchHistory.create_new_search_history(client[0], professional[0])

        return render(request, 'html/search.html', context=context)
