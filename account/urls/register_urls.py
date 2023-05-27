from django.urls import path
from account.views import register_views


urlpatterns = [
    path('', register_views.sign_up, name='register'),
]
