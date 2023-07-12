from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="module.index"),
    path('add/', views.add, name="module.add"),
    path('edit/<int:id>/', views.edit, name="module.edit"),
    path('delete/<int:id>/', views.delete, name="module.delete"),
    path('change-status/<int:id>/', views.status, name='module.status'),
    path('add-more-action/', views.addMoreAction, name="module.add_more_action"),
]
