from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


# Create your models here.
class Languages(CommonModels):
    title = models.CharField(max_length=100, blank=True, null=True)
    lang_code = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    folder_code = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'languages'


class LanguageSetting(CommonModels):
    msgid = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    locale = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    msgstr = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'language_settings'
