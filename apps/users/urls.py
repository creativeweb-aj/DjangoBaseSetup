from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users.index'),
    path('add-new/', views.add, name='users.add'),
    path('edit/<int:id>/', views.edit, name='users.edit'),
    path('view/<int:id>/', views.view, name='users.view'),
    path('delete/<int:id>/', views.delete, name='users.delete'),
    path('change-status/<int:id>/', views.status, name='users.status'),
    path('change-password/<int:id>/', views.changePassword, name='users.change_password'),
    path('send-credentials/<int:id>/', views.sendCredential, name='users.send_credential')
]


