from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request, entity_id):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    return render(request, 'landing/homepage.html')
