from django.urls import path
from apps.api.modules.UserApi import api

urlpatterns = [
    # APIs urls
    path('auth/register', api.register, name="UserApi.api.register"),
    path('auth/login', api.login, name="UserApi.api.login")
]