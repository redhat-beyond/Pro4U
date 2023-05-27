from django.shortcuts import render, redirect
from account.forms import RegisterForm
from account.models.profile import Profile
from account.models.professional import Professions


def sign_up(request):
    professions = Professions.choices
    if request.method == 'GET':
        form1 = RegisterForm()
        return render(request, 'account/register.html', {'form': form1, 'professions': professions})

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            profile = Profile.objects.create(user_id=user, phone_number=form.cleaned_data['phone_number'],
                                             country=form.cleaned_data['country'])
            profile.save()

            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form, 'professions': professions})

