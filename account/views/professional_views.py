from django.shortcuts import render


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    return render(request, 'landing/homepage.html')
