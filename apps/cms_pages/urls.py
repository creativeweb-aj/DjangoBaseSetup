from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="cms_pages.index"),
    path('add', views.add, name="cms_pages.add"),
    path("edit/<id>", views.edit, name='cms_pages.edit'),
    path('view/<id>', views.view, name="cms_pages.view")
]
