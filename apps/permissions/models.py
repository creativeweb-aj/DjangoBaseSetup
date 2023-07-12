from django.db import models
from DjangoBaseSetup.common_modules.models import CommonModels


class AdminModule(CommonModels):
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    path = models.CharField(max_length=250, blank=True, null=True)
    segment = models.CharField(max_length=250, blank=True, null=True)
    module_order = models.PositiveIntegerField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'admin_modules'

    def __str__(self):
        return self.title


class AdminModuleAction(CommonModels):
    admin_module_id = models.ForeignKey(AdminModule, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    function_name = models.CharField(max_length=250, blank=True, null=True)
    is_show = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'admin_modules_actions'

    def __str__(self):
        return self.name
