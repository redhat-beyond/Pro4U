from django.urls import path
from . import views


urlpatterns = [
    path('typeOfJob/', views.typeOfJob_list, name='typeOfJob'),
    path('typeOfJob/create/', views.create_typeOfJob, name='typeOfJob_create'),
    path('typeOfJob/update/<int:pk>/', views.TypeOfJobUpdate.as_view(), name='typeOfJob_update'),
    path('typeOfJob/delete/<int:pk>/', views.TypeOfJobDelete.as_view(), name='typeOfJob_delete'),
]
