from django.shortcuts import render
from account.models.professional import Professional
from django.db.models import Q
from SearchHistory.models import SearchHistory


def search(request, user_id, user_type):
    last_searches = {}
    if user_type == 'C':
        last_searches = SearchHistory.get_last_professionals_search_by_client(client_id=user_id)

    context = {}
    if request.method == 'GET':
        return render(request, 'html/search.html', context=context)

    elif request.method == 'POST':
        professional_id = request.POST.get("professional_id", "")
        profession = request.POST.get("profession", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        city = request.POST.get("city", "")

        professionals = Professional.objects.all()

        if professional_id:
            professionals = professionals.filter(professional_id=professional_id)
        if profession:
            professionals = professionals.filter(profession=profession)
        if first_name:
            professionals = professionals.filter(first_name=first_name)
        if last_name:
            professionals = professionals.filter(last_name=last_name)
        if city:
            professionals = professionals.filter(city=city)

        if professional_id and profession and first_name and last_name and city:
            professionals = professionals.filter(
                Q(professional_id=professional_id) &
                Q(profession=profession) &
                Q(first_name=first_name) &
                Q(last_name=last_name) &
                Q(city=city)
            )

        context['professionals'] = professionals
        context['last_searches'] = last_searches

        return render(request, 'html/search.html', context=context)
