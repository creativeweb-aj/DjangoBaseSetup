from django.contrib.auth.hashers import check_password
from rest_framework import serializers, exceptions
from DjangoBaseSetup.common_modules.mainService import MainService
from DjangoBaseSetup.messages.messages import ValidationMessages
from apps.api.modules.UserApi.service import UserQueryService
from apps.users.models import User


class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile_number', 'password', 'confirm_password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(RegisterUserSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        username = data.get('username', None)
        email = data.get('email', None)
        mobile_number = data.get('mobile_number', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        # Validation Errors
        if first_name == "" or first_name is None:
            error = {
                "field": "first_name",
                "message": ValidationMessages.the_first_name_field_is_required.value
            }
            errors.append(error)

        if last_name == "" or last_name is None:
            error = {
                "field": "last_name",
                "message": ValidationMessages.the_last_name_field_is_required.value
            }
            errors.append(error)

        if username == "" or username is None:
            error = {
                "field": "username",
                "message": ValidationMessages.the_username_field_is_required.value
            }
            errors.append(error)

        if email == "" or email is None:
            error = {
                "field": "email",
                "message": ValidationMessages.the_email_field_is_required.value
            }
            errors.append(error)

        if mobile_number == "" or mobile_number is None:
            error = {
                "field": "mobile_number",
                "message": ValidationMessages.mobile_number_field_required.value
            }
            errors.append(error)

        if password == "" or password is None:
            error = {
                "field": "password",
                "message": ValidationMessages.the_password_field_is_required.value
            }
            errors.append(error)

        if confirm_password == "" or confirm_password is None:
            error = {
                "field": "confirm_password",
                "message": ValidationMessages.the_confirm_password_field_is_required.value
            }
            errors.append(error)

        user = UserQueryService.getUserByUsername(username)
        if user is not None:
            error = {
                "field": "username",
                "message": ValidationMessages.username_is_exist.value
            }
            errors.append(error)

        user = UserQueryService.getUserByEmail(email)
        if user is not None:
            error = {
                "field": "email",
                "message": ValidationMessages.email_is_exist.value
            }
            errors.append(error)

        user = UserQueryService.getUserByMobile(mobile_number)
        if user is not None:
            error = {
                "field": "mobile_number",
                "message": ValidationMessages.mobile_number_exist.value
            }
            errors.append(error)

        if password != confirm_password:
            error = {
                "field": "password",
                "message": ValidationMessages.password_not_match.value
            }
            errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create UserApi
    def create(self, validated_data):
        UserQueryService.createUser(validated_data)
        return validated_data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(LoginUserSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        email = data.get('email', None)
        password = data.get('password', None)

        if email == "" or email is None:
            error = {
                "field": "email",
                "message": ValidationMessages.the_email_field_is_required.value
            }
            errors.append(error)

        if password == "" or password is None:
            error = {
                "field": "password",
                "message": ValidationMessages.the_password_field_is_required.value
            }
            errors.append(error)

        user = UserQueryService.getUserByEmail(email)
        if user is None:
            error = {
                "field": "email",
                "message": ValidationMessages.email_is_not_exist.value
            }
            errors.append(error)
        else:
            if not check_password(password, user.password):
                error = {
                    "field": "password",
                    "message": ValidationMessages.password_not_match.value
                }
                errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'mobile_number', 'image',
                  'user_role_id', 'city', 'state', 'country', 'zip_code',
                  'address1', 'address2', 'is_active']
