from django.shortcuts import render, get_object_or_404
from account.models.client import Client


def show_profile(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'account/client_profile.html', {'client': client})
