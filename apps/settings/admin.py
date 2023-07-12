from django.contrib import admin
from apps.settings.models import Setting


class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'key', 'value', 'input_type')


admin.site.register(Setting, SettingAdmin)
