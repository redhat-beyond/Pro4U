from django.urls import path
from . import views


urlpatterns = [
    path("calendar/<int:professional>",  views.CalendarView.as_view(), name="calendar"),
    path("schedule_new/<int:professional>", views.create_schedule, name="schedule_new"),
    path("schedule/<int:schedule_id>/details/", views.schedule_details, name="schedule_detail"),
    path("schedule/edit/<int:pk>/", views.ScheduleEdit.as_view(), name="schedule_edit"),
    path("schedule/<int:pk>/remove", views.ScheduleDeleteView.as_view(), name="remove_schedule"),
]
