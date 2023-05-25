from django.shortcuts import render, get_object_or_404
from account.models.professional import Professional
from reservation.models import TypeOfJob


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    return render(request, 'landing/homepage.html')


def show_business_page(request, professional_id):
    if request.user.is_authenticated:
        professional = get_object_or_404(Professional, pk=professional_id)
        typeOfjobs_by_pro = TypeOfJob.get_typeofjobs_by_professional(professional_id=professional.professional_id)
        context = {'professional': professional, 'typeOfjobs_by_pro': typeOfjobs_by_pro}
        return render(request, 'account/business_page.html', context)
    return render(request, 'landing/homepage.html')