from rest_framework import serializers, exceptions
from apps.cms_pages.models import CmsPages


class CmsPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsPages
        fields = ['id', 'page_name', 'page_title', 'description']
