from django.urls import path
from account.views import profile_views


urlpatterns = [
    path('profile/professional/<int:professional_id>/', profile_views.show_business_page, name='show_business_page'),
    path('profile/', profile_views.user_profile, name='user_profile'),
    path('profile/settings/', profile_views.show_settings, name='show_settings'),
    path('profile/edit/', profile_views.edit_profile, name='edit_profile'),
]
