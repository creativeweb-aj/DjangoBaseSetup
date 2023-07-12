from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


class CmsPages(CommonModels):
    page_name = models.CharField(max_length=255, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cms_pages'


class CmsPageDescriptions(CommonModels):
    cms_page = models.ForeignKey(CmsPages, on_delete=models.CASCADE, blank=True, null=True)
    language_code = models.CharField(db_index=True, max_length=20, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cms_page_descriptions'
