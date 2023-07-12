from django.contrib.auth.hashers import make_password
from apps.users.models import User
from django.utils.timezone import datetime  # important if using timezones

today = datetime.today()


class UserQuery:
    def __init__(self):
        pass

    # Get user data by email id
    @staticmethod
    def getUserByEmail(email: str):
        try:
            user = User.objects.get(email=email, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Get user data by email id
    @staticmethod
    def getUserBySocialId(socialId: str):
        try:
            user = User.objects.get(social_id=socialId, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Get user data by email id
    @staticmethod
    def getUserByOtp(otp: str):
        try:
            user = User.objects.get(forgot_password_otp=otp, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Check user exist or not by mobile number
    @staticmethod
    def getUserByMobileNumber(number: str):
        try:
            user = User.objects.get(mobile_number=number, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Get user by user id
    @staticmethod
    def getUserById(userId: int):
        try:
            user = User.objects.get(id=userId, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Create user or save user data
    @staticmethod
    def createUser(data: dict()):
        try:
            user = User()
            user.name = data.get('name', '')
            user.user_role_id = 2
            user.mobile_number = data.get('mobile_number', '')
            user.email = data.get('email', '')
            user.password = make_password(data.get('password', ''))
            user.confirm_password = data.get('confirm_password', '')
            user.social_type = data.get('social_type', '')
            user.social_id = data.get('social_id', '')
            user.save()
        except Exception as e:
            user = None
        return user

    # Update user password
    @classmethod
    def updateUserPassword(cls, data: dict()):
        try:
            user = cls.getUserById(data['user_id'])
            user.forgot_password_otp = None
            user.password = make_password(data['new_password'])
            user.confirm_password = data['confirm_password']
            user.save()
        except Exception as e:
            user = None
        return user

    # Create patient_user
    @staticmethod
    def createPatientUser(data: dict):
        try:
            user = User()
            user.user_role_id = 2
            user.mobile_number = data.get('mobile_number', '')
            user.email = data.get('email', '')
            user.password = make_password(data.get('password', None))
            user.confirm_password = data.get('password', None)
            user.save()
        except Exception as e:
            user = None
        return user
