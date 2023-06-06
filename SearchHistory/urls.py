from django.urls import path
from . import views
from account.views.profile_views import show_business_page


urlpatterns = [
    path('search/<int:user_id>/', views.search, name='search history'),
    path('profile/professional/<int:professional_id>/', show_business_page, name='show professional')
]
