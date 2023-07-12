from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('logout/', views.logOut, name="logout"),
    path('myaccount/', views.profile, name="login.myaccount"),
    path('change-password/', views.updatePassword, name="login.change_password"),
    path('forgot-password/', views.forgotPassword, name="login.forgot_password"),
    path('forgot-password-otp/', views.passwordResetOtp, name="login.password_reset_otp"),
    path('reset-password/<token>/', views.passwordReset, name='login.reset_password')
]
