from django.urls import path
from . import views


urlpatterns = [
    path('SearchHistory/', views.search, name='search history')
]
