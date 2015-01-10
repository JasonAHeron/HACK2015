from django.contrib import admin
# Import the UserProfile model individually.
from hack.models import UserProfile

# Register your models here.
admin.site.register(UserProfile)