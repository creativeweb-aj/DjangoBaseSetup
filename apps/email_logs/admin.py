from django.contrib import admin
from .models import EmailLog
from django.utils.html import mark_safe


# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_from', 'email_to', 'newHtmlMessage', 'created_at', 'updated_at')

    @staticmethod
    def newHtmlMessage(obj):
        # return HTML links that will not be escaped
        return mark_safe(obj.message)


admin.site.register(EmailLog, EmailAdmin)
