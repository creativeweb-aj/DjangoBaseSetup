from django.contrib import admin
from .models import User
# from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at', 'is_active', 'user_role_id')


admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
