from django.contrib import admin
from .models.profile import Profile
from .models.professional import Professional
from .models.client import Client


admin.site.register(Profile)
admin.site.register(Professional)
admin.site.register(Client)
