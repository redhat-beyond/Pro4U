from django.shortcuts import render, get_object_or_404


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    return render(request, 'homepage.html')
