from django.shortcuts import render, get_object_or_404
from account.models.client import Client


def show_profile(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    profile = client.profile_id
    return render(request, 'account/profile.html', {'client': client, 'profile': profile})
