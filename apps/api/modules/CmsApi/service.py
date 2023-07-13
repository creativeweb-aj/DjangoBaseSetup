from apps.api.modules.CmsApi.serializer import CmsPageSerializer
from apps.cms_pages.models import CmsPages


class CmsService:
    def __init__(self):
        pass

    @staticmethod
    def getCmsData(slug: str) -> any:
        try:
            cmsPage = CmsPages.objects.filter(slug=slug).first()
        except Exception as e:
            print(f"Exception (getCmsData) --> {e}")
            cmsPage = None
        # Serialize data
        cmsPageSerializer = CmsPageSerializer(cmsPage)
        data = cmsPageSerializer.data.get('description', None)
        return data

