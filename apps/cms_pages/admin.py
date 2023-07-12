from django.contrib import admin
from .models import CmsPages, CmsPageDescriptions


# Register your models here.
class CmsPageAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'page_title', 'created_at', 'updated_at')


class CmsPageDescriptionAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'language_code', 'description')


admin.site.register(CmsPages, CmsPageAdmin)
admin.site.register(CmsPageDescriptions, CmsPageDescriptionAdmin)
