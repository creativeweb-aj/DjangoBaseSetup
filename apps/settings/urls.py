from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="settings.index"),
    path('add-setting/', views.add, name="settings.add"),
    path("edit-setting/<int:id>/", views.edit, name='settings.edit'),
    path("delete-setting/<id>", views.delete, name='settings.delete'),
    path("prefix/<key>", views.prefix, name='settings.prefix'),
]

