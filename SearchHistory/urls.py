from django.urls import path
from . import views


urlpatterns = [
    path('search/<int:user_id>/<str:user_type>/', views.search, name='search history')
]
