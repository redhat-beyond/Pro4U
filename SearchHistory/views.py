import json
from django.shortcuts import render
from account.models.professional import Professional
from django.db.models import Q
from SearchHistory.models import SearchHistory
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required


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
        professionals = Professional.objects.all()

        professional_id = request.POST.get("professional_id", "")
        profession = request.POST.get("profession", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        city = request.POST.get("city", "")
        # professional_id_searched = request.POST.get("professional_id_searched", "")
        # SearchHistory.create_new_search_history(client_id=user_id, professional_id=professional_id_searched)

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

        return render(request, 'html/search.html', context=context)


@permission_required('your_app.create_search_history')
def create_search_history(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data['client_id']
        professional_id = data['professional_id']

        SearchHistory.create_new_search_history(client_id=client_id, professional_id=professional_id)
        # Perform the necessary logic with the professional ID

        # Return a JSON response indicating the success or failure of the operation
        return JsonResponse({'message': 'Search history created successfully.'})
