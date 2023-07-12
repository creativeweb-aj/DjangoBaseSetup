from django.contrib import admin
from .models import *
from django.utils.html import mark_safe


class EmailActionAdmin(admin.ModelAdmin):
    list_display = ('id','action', 'created_at', 'is_active')


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'html_body', 'action', 'created_at', 'updated_at')

    @staticmethod
    def html_body(obj):
        # return HTML link that will not be escaped
        return mark_safe(obj.body)


class EmailDescAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'html_body_desc', 'language_code', 'updated_at')

    @staticmethod
    def html_body_desc(obj):
        # return HTML link that will not be escaped
        return mark_safe(obj.description)


admin.site.register(EmailActions, EmailActionAdmin)
admin.site.register(EmailTemplates, EmailTemplateAdmin)
admin.site.register(EmailTemplatesDescription, EmailDescAdmin)
