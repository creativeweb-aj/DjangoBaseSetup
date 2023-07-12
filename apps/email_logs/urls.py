from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="email_logs.index"),
    path('view/<int:id>/', views.view, name='email_logs.view')
]

