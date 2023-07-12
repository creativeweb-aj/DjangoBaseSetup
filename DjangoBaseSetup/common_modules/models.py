from django.db import models
from django.utils import timezone


class CommonModels(models.Model):
    """
    An abstract base class for all models
    Add created and modified fields for all models
    """
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
