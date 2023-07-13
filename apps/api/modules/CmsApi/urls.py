from django.urls import path
from apps.api.modules.CmsApi import api

urlpatterns = [
    # APIs urls
    path('CmsApi/privacy-policy', api.privacyPolicy, name="CmsApi.api.privacy_policy"),
    path('CmsApi/terms-condition', api.termsConditions, name="CmsApi.api.terms_condition"),
    path('CmsApi/about', api.about, name="CmsApi.api.about")
]
