from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models.profile import UserType
from account.forms import UserUpdateForm, ProfileUpdateForm
from account.models.professional import Professional
from reservation.models import TypeOfJob
from review.models import Review


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
        typeOfJobs_by_pro = TypeOfJob.get_typeofjobs_by_professional(professional_id=professional.professional_id)
        # Reviews
        reviews = Review.filter_by_professional(professional=professional_id)
        one_star_reviews = reviews.filter(rating=Review.Rating.ONE_STAR[0])
        two_star_reviews = reviews.filter(rating=Review.Rating.TWO_STARS[0])
        three_star_reviews = reviews.filter(rating=Review.Rating.THREE_STARS[0])
        four_star_reviews = reviews.filter(rating=Review.Rating.FOUR_STARS[0])
        five_star_reviews = reviews.filter(rating=Review.Rating.FIVE_STARS[0])
        total_reviews = reviews.count()
        if total_reviews == 0:
            one_star_percent = 0
            two_star_percent = 0
            three_star_percent = 0
            four_star_percent = 0
            five_star_percent = 0
        else:
            one_star_percent = one_star_reviews.count() / total_reviews
            two_star_percent = two_star_reviews.count() / total_reviews
            three_star_percent = three_star_reviews.count() / total_reviews
            four_star_percent = four_star_reviews.count() / total_reviews
            five_star_percent = five_star_reviews.count() / total_reviews
        context = {
            'professional': professional,
            'typeOfjobs_by_pro': typeOfJobs_by_pro,
            'reviews': total_reviews,
            'ONE': one_star_reviews.count(),
            'TWO': two_star_reviews.count(),
            'THREE': three_star_reviews.count(),
            'FOUR': four_star_reviews.count(),
            'FIVE': five_star_reviews.count(),
            'ONE_PERCENT': one_star_percent * 100,
            'TWO_PERCENT': two_star_percent * 100,
            'THREE_PERCENT': three_star_percent * 100,
            'FOUR_PERCENT': four_star_percent * 100,
            'FIVE_PERCENT': five_star_percent * 100,
            'AVG': Review.get_professional_avg_rating(professional=professional_id)
        }
        return render(request, 'account/business_page.html', context)
    return render(request, 'landing/homepage.html')
