from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


class Setting(CommonModels):
    title = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    value = models.TextField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    input_type = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    editable = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'settings'
