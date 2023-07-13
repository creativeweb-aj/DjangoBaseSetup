from django.urls import path
from apps.api.modules.CmsApi import api

urlpatterns = [
    # APIs urls
    path('CmsApi/privacy-policy', CmsApi.privacyPolicy, name="CmsApi.api.privacy_policy"),
    path('CmsApi/terms-condition', CmsApi.termsConditions, name="CmsApi.api.terms_condition"),
    path('CmsApi/about', CmsApi.about, name="CmsApi.api.about")
]
