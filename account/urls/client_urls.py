from django.urls import path
from account.views import client_views

urlpatterns = [
    path('profile/<int:client_id>/', client_views.show_profile, name='show_profile'),
]
