from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, User_profile

# Register your models here.
admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(User_profile)
