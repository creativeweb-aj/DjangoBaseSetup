from django.urls import path
from apps.api.modules.user import UserApi

urlpatterns = [
    # APIs urls
    path('auth/login-with-mobile', UserApi.mobileLogin, name="user.api.login_with_mobile"),
    path('auth/verify-mobile', UserApi.verifyMobileLogin, name="user.api.verify_mobile"),
    path('auth/resend-otp', UserApi.resendOtp, name="user.api.resend_otp"),
    path('auth/social-login', UserApi.socialLogin, name="user.api.social_login"),
    path('secure/profile', UserApi.userProfile, name="user.api.profile"),
    path('secure/update-profile', UserApi.updateProfile, name="user.api.update_profile"),
    path('secure/add-profile', UserApi.addProfile, name="user.api.add_profile"),
    # path('secure/update-profile-image', UserApi.updateProfileImage, name="user.api.update_profile_image"),
    path('secure/my-profiles', UserApi.myProfiles, name="user.api.my_profiles"),
    path('secure/child-profile/<int:Id>', UserApi.childProfile, name="user.api.child_profile"),
    path('secure/delete-profile/<int:Id>', UserApi.deleteChildProfile, name="user.api.delete_profile"),
    path('secure/update-child-profile/<int:Id>', UserApi.updateChildProfile, name="user.api.update_child_profile"),
]
