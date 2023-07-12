from django.contrib import admin
from .models import *


# Register your models here.

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at', 'updated_at')


class FaqAdminDescriptions(admin.ModelAdmin):
    list_display = ('faq', 'language_code', 'question', 'answer')


admin.site.register(Faq, FaqAdmin)
admin.site.register(FaqDescriptions, FaqAdminDescriptions)
