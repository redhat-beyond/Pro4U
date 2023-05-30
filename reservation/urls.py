from django.urls import path
from . import views


urlpatterns = [
    path('typeOfJob/', views.typeOfJob_list, name='typeOfJob'),
    path('typeOfJob/create/', views.create_typeOfJob, name='typeOfJob_create'),
    path('typeOfJob/update/<int:pk>/', views.TypeOfJobUpdate.as_view(), name='typeOfJob_update'),
    path('typeOfJob/delete/<int:pk>/', views.type_of_job_delete, name='typeOfJob_delete'),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("schedule_new/", views.create_schedule, name="schedule_new"),
    path("schedule/<int:schedule_id>/details/", views.schedule_details, name="schedule_detail"),
    path("schedule/edit/<int:pk>/", views.ScheduleEdit.as_view(), name="schedule_edit"),
    path("schedule/<int:pk>/remove", views.ScheduleDeleteView.as_view(), name="remove_schedule"),
]
