from django.urls import path
from account.views import login_views

urlpatterns = [
     path('login/', login_views.sign_in, name='login'),
]
