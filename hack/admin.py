from django.contrib import admin
# Import the UserProfile model individually.
from hack.models import UserProfile
from .models import Request

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Request)