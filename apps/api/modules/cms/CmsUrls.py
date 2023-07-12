from django.urls import path
from apps.api.modules.cms import CmsApi

urlpatterns = [
    # APIs urls
    path('cms/privacy-policy', CmsApi.privacyPolicy, name="cms.api.privacy_policy"),
    path('cms/terms-condition', CmsApi.termsConditions, name="cms.api.terms_condition"),
    path('cms/about', CmsApi.about, name="cms.api.about")
]
