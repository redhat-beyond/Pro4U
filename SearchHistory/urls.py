from django.urls import path
from . import views


urlpatterns = [
    path('search/<int:user_id>/', views.search, name='search history')
    # path('create_search_history/', views.create_search_history, name='create_search_history')

]
