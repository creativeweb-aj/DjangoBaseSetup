from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="email_templates.index"),
	path('add/', views.add, name="email_templates.add"),
	path("edit/<id>", views.edit, name='email_templates.edit'),
	path('constants/', views.getConstant, name='email_templates.constants'),
]

