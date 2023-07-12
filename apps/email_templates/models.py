from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


class EmailActions(CommonModels):
    action = models.CharField(max_length=255, blank=True, null=True)
    option = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'email_actions'


class EmailTemplates(CommonModels):
    name = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'email_templates'


class EmailTemplatesDescription(CommonModels):
    email_template = models.ForeignKey(EmailTemplates, on_delete=models.CASCADE, blank=True, null=True)
    language_code = models.CharField(db_index=True, max_length=20, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'email_templates_descriptions'
