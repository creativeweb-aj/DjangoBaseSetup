from django.contrib import admin

# Register your models here.
from .models import AdminModule, AdminModuleAction


class AdminModuleCustom(admin.ModelAdmin):
    list_display = ('title', 'path', 'module_order', 'parent_id', 'created_at','id')


admin.site.register(AdminModule, AdminModuleCustom)


class AdminModuleActionCustom(admin.ModelAdmin):
    list_display = ('name', 'function_name', 'admin_module_id', 'is_show', 'created_at')


admin.site.register(AdminModuleAction, AdminModuleActionCustom)
