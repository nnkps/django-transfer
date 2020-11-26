from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProtectedItem, User

UserAdmin.list_display += ("user_agent",)

admin.site.register(User, UserAdmin)
admin.site.register(ProtectedItem)
