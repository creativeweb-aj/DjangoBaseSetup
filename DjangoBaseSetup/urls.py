"""DjangoBaseSetup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from DjangoBaseSetup.common_modules.mainService import MainService

urlpatterns = [
    # APIs
    path('api/', include('apps.api.urls')),

    # Admin panel URL
    path('admin/', admin.site.urls),

    # Base Admin Apps
    path('', include('apps.login.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('users/', include('apps.users.urls')),
    path('CmsApi-manager/', include('apps.cms_pages.urls')),
    path('email-manager/', include('apps.email_templates.urls')),
    path('email-logs/', include('apps.email_logs.urls')),
    path('settings/', include('apps.settings.urls')),
    path('acl/', include('apps.permissions.urls')),
    path('faq/', include('apps.faq.urls')),

    # Project Apps
]

handler404 = MainService.error_404
handler500 = MainService.error_500
handler403 = MainService.error_403
handler400 = MainService.error_400

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
