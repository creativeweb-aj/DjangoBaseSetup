from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


class EmailLog(CommonModels):
    email_to = models.CharField(max_length=100, blank=True, null=True)
    email_from = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'email_logs'
