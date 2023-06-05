from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models.profile import UserType
from account.forms import UserUpdateForm, ProfileUpdateForm
from account.models.professional import Professional
from reservation.models import TypeOfJob


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    return render(request, 'landing/homepage.html')



@login_required
def show_settings(request):
    if request.user.is_authenticated:
        user_types = UserType
        context = {'user_types': user_types}
        return render(request, 'account/profile_details.html', context)
    return render(request, 'landing/homepage.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile/settings/')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit_profile.html', context)


def show_business_page(request, professional_id):
    if request.user.is_authenticated:
        professional = get_object_or_404(Professional, pk=professional_id)
        typeOfjobs_by_pro = TypeOfJob.get_typeofjobs_by_professional(professional_id=professional.professional_id)
        context = {'professional': professional, 'typeOfjobs_by_pro': typeOfjobs_by_pro}
        return render(request, 'account/business_page.html', context)
    return render(request, 'landing/homepage.html')
