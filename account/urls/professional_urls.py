from django.urls import path
from account.views import professional_views

urlpatterns = [
    path('profile/<int:professional_id>/', professional_views.show_profile, name='show_profile'),
]
