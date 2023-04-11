from django.contrib import admin
from .models import TypeOfJob, Appointment, Schedule

admin.site.register(TypeOfJob)
admin.site.register(Appointment)
admin.site.register(Schedule)

