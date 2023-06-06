from django.urls import path
from account.views import profile_views


urlpatterns = [
    path('profile/', profile_views.user_profile, name='user_profile'),
]
