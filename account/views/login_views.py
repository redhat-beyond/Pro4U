from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from account.forms import LoginForm
from account.models.professional import Professional


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
                professional = Professional.objects.filter(profile_id__user_id=request.user)[0]
                professional_id = professional.professional_id
                return redirect('show_profile', professional_id=professional_id)
        messages.error(request, 'Invalid username or password')
        return render(request, 'account/login.html', {'form': form})
