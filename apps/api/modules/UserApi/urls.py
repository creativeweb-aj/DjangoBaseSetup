from django.urls import path
from apps.api.modules.UserApi import api

urlpatterns = [
    # APIs urls
    path('auth/register', UserApi.register, name="UserApi.api.register"),
    path('auth/login', UserApi.login, name="UserApi.api.login")
]