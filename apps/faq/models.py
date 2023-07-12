from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


# Create your models here.
class Faq(CommonModels):
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'faqs'


class FaqDescriptions(CommonModels):
    faq = models.ForeignKey(Faq, on_delete=models.CASCADE, blank=True, null=True)
    language_code = models.CharField(db_index=True, max_length=20, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'faq_descriptions'
