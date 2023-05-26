from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from account.forms import LoginForm
from account.models.professional import Professional
from account.models.client import Client


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                # I'll change it when we have the proper page
                professional_queryset = Professional.objects.filter(profile_id__user_id=request.user)
                if professional_queryset.exists():
                    professional = professional_queryset.first()
                    professional_id = professional.professional_id
                    return redirect('profile_urls:user_profile', entity_id=professional_id)
                else:
                    client = Client.objects.filter(profile_id__user_id=request.user)[0]
                    client_id = client.client_id
                    return redirect('profile_urls:user_profile', entity_id=client_id)

        messages.error(request, 'Invalid username or password')
        return render(request, 'account/login.html', {'form': form})
