from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="faqs.index"),
    path('add/', views.add, name="faqs.add"),
    path("edit/<id>", views.edit, name='faqs.edit'),
    path("change-status/<id>", views.status, name='faqs.status'),
    path('delete/<int:id>/', views.delete, name='faqs.delete')
]

