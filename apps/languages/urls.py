from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="languages.index"),
    path("edit/<id>", views.edit, name='languages.edit'),
]

