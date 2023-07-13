from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        schema.basePath = '/api' + schema.basePath
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Django Base App APIs",
        default_version='V1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny],
    urlconf="apps.api.urls"
)

urlpatterns = [
    # Swagger Doc
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # APIs urls
    path('v1/', include('apps.api.modules.UserApi.urls')),
    path('v1/', include('apps.api.modules.CmsApi.urls'))
]
