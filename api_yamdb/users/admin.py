from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'bio', 'email', 'role')
    list_editable = ('role',)