import datetime
from apps.api.modules.user.UserService import UserQueryService
from DjangoBaseSetup.messages.messages import ValidationMessages
from rest_framework import serializers, exceptions
from apps.users.models import User
from django.contrib.auth.hashers import check_password
from DjangoBaseSetup.common_modules.mainService import MainService
from DjangoBaseSetup import settings


class CreateUsersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile_number', 'password', 'confirm_password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(CreateUsersSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        name = data.get('name', None)
        email = data.get('email', None)
        mobile_number = data.get('mobile_number', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        # Validation Errors
        if name == "" or name is None:
            error = {
                "field": "name",
                "message": ValidationMessages.the_name_field_is_required.value
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

        email = UserQueryService.getUserByEmail(email)
        if email is not None:
            error = {
                "field": "email",
                "message": ValidationMessages.emailIsExist.value
            }
            errors.append(error)
        mobile_number = UserQueryService.getUserByMobileNumber(mobile_number)

        if mobile_number is not None:
            error = {
                "field": "mobile_number",
                "message": ValidationMessages.mobile_number_exist.value
            }
            errors.append(error)

        if password != confirm_password:
            error = {
                "field": "password",
                "message": ValidationMessages.passNotMatch.value
            }
            errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create user
    def create(self, validated_data):
        userData = {
            'name': validated_data.get('name'),
            'mobile_number': validated_data.get('mobile_number'),
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
            'confirm_password': validated_data.get('confirm_password'),
        }
        UserQueryService.createUser(userData)
        return validated_data


class MobileLoginSerializer(serializers.ModelSerializer):
    mobile_number = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['mobile_number']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(MobileLoginSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        mobile_number = int(data.get('mobile_number', None))
        if mobile_number == "" or mobile_number is None:
            error = {
                "field": "mobile_number",
                "message": ValidationMessages.mobile_number_field_required.value
            }
            errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create user
    def create(self, validated_data):
        UserQueryService.createUpdateUserMobileLogin(validated_data)
        return validated_data


class VerifyMobileLoginSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    mobile_otp = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['user_id', 'mobile_otp']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(VerifyMobileLoginSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        user_id = data.get('user_id', None)
        mobile_otp = int(data.get('mobile_otp', None))
        if user_id == "" or user_id is None:
            error = {
                "field": "user_id",
                "message": ValidationMessages.user_id_required.value
            }
            errors.append(error)
        if mobile_otp == "" or mobile_otp is None or mobile_otp == 0:
            error = {
                "field": "mobile_otp",
                "message": ValidationMessages.mobile_otp_required.value
            }
            errors.append(error)
        if user_id and mobile_otp:
            user = UserQueryService.getUserById(user_id)
            if user is None:
                error = {
                    "field": "user_id",
                    "message": ValidationMessages.userIsNotExist.value
                }
                errors.append(error)
            else:
                if user.mobile_otp and int(user.mobile_otp) != 0:
                    if user.mobile_otp != mobile_otp:
                        error = {
                            "field": "mobile_otp",
                            "message": ValidationMessages.mobileOtpNotMatch.value
                        }
                        errors.append(error)
                else:
                    isUserOtpExpired = UserQueryService.checkOtpExpireById(user_id)
                    if isUserOtpExpired is None:
                        error = {
                            "field": "mobile_otp",
                            "message": ValidationMessages.mobileOtpIsExpire.value
                        }
                        errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'mobile_number',
                  'user_role_id', 'city', 'state', 'country', 'zip_code',
                  'address1', 'address2', 'latitude', 'longitude']


class PatientSerializer(serializers.ModelSerializer):
    patient_id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    relationship = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['patient_id', 'mrd_no', 'user', 'parent_id', 'image', 'full_name', 'mobile_number', 'email',
                  'gender', 'dob', 'age', 'address', 'relationship', 'latitude', 'longitude', 'is_parent', 'updated_at']

    def get_patient_id(self, obj):
        return obj.id

    def get_email(self, obj):
        if obj:
            if obj.email:
                if "@mobile" in obj.email:
                    return None
                else:
                    return obj.email
            else:
                return None
        else:
            return None

    def get_user(self, obj):
        user = User.objects.filter(id=obj.user_id.id, is_active=True).first()
        userSerializer = UserSerializer(instance=user)
        return userSerializer.data

    def get_relationship(self, obj):
        if obj.relationship:
            name = obj.relationship.name
        else:
            name = None
        return name

    def get_age(self, obj):
        age = None
        if obj.dob:
            dob = obj.dob
            print(f"dob --> {dob}")
            today = datetime.date.today()
            print(f"today --> {today}")
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    def get_image(self, obj):
        if obj:
            if str(obj.image):
                return str(settings.BASE_URL)+str(obj.image.url)
            else:
                return MainService.getDefaultImages("user")
        else:
            return MainService.getDefaultImages("user")


GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)


class UpdatePatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True)
    dob = serializers.DateField(required=True)
    address = serializers.CharField(required=True)
    relationship = serializers.IntegerField(required=False)
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)

    class Meta:
        model = Patient
        fields = ['full_name', 'mobile_number', 'email', 'gender', 'dob', 'address', 'relationship', 'image', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UpdatePatientSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        currUser = self.context['request'].user
        fullName = data.get('full_name', None)
        mobileNumber = data.get('mobile_number', None)
        email = data.get('email', None)
        gender = data.get('gender', None)
        dob = data.get('dob', None)
        address = data.get('address', None)
        # relationship = data.get('relationship', None)
        image = data.get('image', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)

        if fullName == "" or fullName is None:
            error = {
                "field": "full_name",
                "message": ValidationMessages.full_name_required.value
            }
            errors.append(error)

        if email is None or email == "":
            error = {
                "field": "email",
                "message": ValidationMessages.email_required.value
            }
            errors.append(error)
        else:
            if currUser and currUser.email != email:
                user = UserQueryService.getUserByEmailCheckAll(email)
                if user:
                    error = {
                        "field": "email",
                        "message": ValidationMessages.emailIsExist.value
                    }
                    errors.append(error)

        if mobileNumber is None or mobileNumber == "":
            error = {
                "field": "mobile_number",
                "message": ValidationMessages.mobile_number_required.value
            }
            errors.append(error)
        else:
            print(f"user --> {currUser}")
            if currUser and currUser.mobile_number != mobileNumber:
                user = UserQueryService.getUserByMobileNumber(mobileNumber)
                if user:
                    error = {
                        "field": "mobile_number",
                        "message": ValidationMessages.mobile_number_exist.value
                    }
                    errors.append(error)

        if gender == "" or gender is None:
            error = {
                "field": "gender",
                "message": ValidationMessages.gender_required.value
            }
            errors.append(error)

        if dob == "" or dob is None:
            error = {
                "field": "dob",
                "message": ValidationMessages.dob_required.value
            }
            errors.append(error)

        if address == "" or address is None:
            error = {
                "field": "address",
                "message": ValidationMessages.address_required.value
            }
            errors.append(error)

        if latitude == "" or latitude is None:
            error = {
                "field": "latitude",
                "message": ValidationMessages.latitude_required.value
            }
            errors.append(error)

        if longitude == "" or longitude is None:
            error = {
                "field": "longitude",
                "message": ValidationMessages.longitude_required.value
            }
            errors.append(error)

        if image:
            allowedImageFormats = ['jpg', 'png', 'PNG', 'JPEG', 'jpeg']
            fileFormat = str(image).split('.')[-1]
            if fileFormat not in allowedImageFormats:
                error = {
                    "field": "image",
                    "message": ValidationMessages.the_image_format_not_allowed.value
                }
                errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create user
    def update(self, instance, validated_data):
        print(f"instance.id --> {instance.id}")
        validated_data['patient_id'] = instance.id
        print(f"validated_data --> {validated_data}")
        # Update user password
        UserQueryService.updatePatientUserProfile(validated_data)
        return validated_data


class AddPatientSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=True)
    full_name = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True)
    dob = serializers.DateField(required=True)
    address = serializers.CharField(required=True)
    relationship = serializers.IntegerField(required=True)
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)

    class Meta:
        model = Patient
        fields = ['parent_id', 'full_name', 'mobile_number', 'email', 'gender', 'dob', 'address',
                  'relationship', 'image', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(AddPatientSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        currUser = self.context['request'].user
        data['user'] = self.context['request'].user
        parentId = data.get('parent_id', None)
        fullName = data.get('full_name', None)
        mobileNumber = data.get('mobile_number', None)
        email = data.get('email', None)
        gender = data.get('gender', None)
        image = data.get('image', None)
        dob = data.get('dob', None)
        address = data.get('address', None)
        relationship = data.get('relationship', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)

        if parentId == "" or parentId is None:
            error = {
                "field": "parent_id",
                "message": ValidationMessages.parent_id_required.value
            }
            errors.append(error)

        if fullName == "" or fullName is None:
            error = {
                "field": "full_name",
                "message": ValidationMessages.full_name_required.value
            }
            errors.append(error)

        if mobileNumber == "" or mobileNumber is None:
            error = {
                "field": "mobile_number",
                "message": ValidationMessages.mobile_number_required.value
            }
            errors.append(error)
        else:
            print(f"user --> {currUser}")
            if currUser and currUser.mobile_number != mobileNumber:
                user = Patient.objects.filter(mobile_number=mobileNumber, is_active=True).first()
                if user:
                    error = {
                        "field": "mobile_number",
                        "message": ValidationMessages.mobile_number_exist.value
                    }
                    errors.append(error)

        if email == "" or email is None:
            error = {
                "field": "email",
                "message": ValidationMessages.email_required.value
            }
            errors.append(error)
        else:
            if currUser and currUser.email != email:
                user = Patient.objects.filter(email=email, is_active=True).first()
                if user:
                    error = {
                        "field": "email",
                        "message": ValidationMessages.emailIsExist.value
                    }
                    errors.append(error)

        if gender == "" or gender is None:
            error = {
                "field": "gender",
                "message": ValidationMessages.gender_required.value
            }
            errors.append(error)

        if dob == "" or dob is None:
            error = {
                "field": "dob",
                "message": ValidationMessages.dob_required.value
            }
            errors.append(error)

        if address == "" or address is None:
            error = {
                "field": "address",
                "message": ValidationMessages.address_required.value
            }
            errors.append(error)

        if relationship == "" or relationship is None:
            error = {
                "field": "relationship",
                "message": ValidationMessages.relationship_required.value
            }
            errors.append(error)
        else:
            relationshipObj = MasterService.getRelationshipById(int(relationship))
            if relationshipObj is None:
                error = {
                    "field": "relationship",
                    "message": ValidationMessages.relationship_not_found.value
                }
                errors.append(error)

        if latitude == "" or latitude is None:
            error = {
                "field": "latitude",
                "message": ValidationMessages.latitude_required.value
            }
            errors.append(error)

        if longitude == "" or longitude is None:
            error = {
                "field": "longitude",
                "message": ValidationMessages.longitude_required.value
            }
            errors.append(error)

        if image == "" or image is None:
            error = {
                "field": "image",
                "message": ValidationMessages.the_profile_image_is_required.value
            }
            errors.append(error)
        else:
            allowedImageFormats = ['jpg', 'png', 'PNG', 'JPEG', 'jpeg']
            fileFormat = str(image).split('.')[-1]
            if fileFormat not in allowedImageFormats:
                error = {
                    "field": "image",
                    "message": ValidationMessages.the_image_format_not_allowed.value
                }
                errors.append(error)

        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create user
    def create(self, validated_data):
        print(f"validated_data--> {validated_data}")
        # Update user password
        UserQueryService.addPatientUserProfile(validated_data)
        return validated_data


class ResendOtpSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['user_id']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(ResendOtpSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate data
    def validate(self, data):
        errors = []
        user_id = int(data.get('user_id', None))
        if user_id == "" or user_id is None:
            error = {
                "field": "user_id",
                "message": ValidationMessages.user_id_required.value
            }
            errors.append(error)
        else:
            user_id = UserQueryService.getUserById(user_id)
            if user_id is None:
                error = {
                    "field": "user_id",
                    "message": ValidationMessages.userIsExist.value
                }
                errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Create user
    def create(self, validated_data):
        UserQueryService.updateUserMobileOtp(validated_data)
        return validated_data


class SocialLoginSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)
    mobile_number = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(allow_blank=True, required=False)
    confirm_password = serializers.CharField(allow_blank=True, required=False)
    social_type = serializers.CharField(allow_blank=False, required=True)
    social_id = serializers.CharField(allow_blank=False, required=True)

    class Meta:
        fields = ['name', 'email', 'mobile_number', 'password', 'confirm_password', 'social_type', 'social_id']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(SocialLoginSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate request data
    def validate(self, data):
        errors = []
        socialType = data.get('social_type', '')
        socialId = data.get('social_id', '')
        email = data.get('email', '')
        mobileNumber = data.get('mobile_number', '')

        if socialType is None or socialType == "":
            error = {
                "field": "social_type",
                "message": ValidationMessages.socialTypeRequired.value
            }
            errors.append(error)
        if socialId is None or socialId == "":
            error = {
                "field": "social_id",
                "message": ValidationMessages.socialIdRequired.value
            }
            errors.append(error)
        # if email is None or email == "":
        #     error = {
        #         "field": "email",
        #         "message": ValidationMessages.email_required.value
        #     }
        #     errors.append(error)
        # else:
        #     user = UserQueryService.getUserByEmail(email)
        #     if user:
        #         error = {
        #             "field": "email",
        #             "message": ValidationMessages.emailIsExist.value
        #         }
        #         errors.append(error)
        # if mobileNumber is None or mobileNumber == "":
        #     error = {
        #         "field": "mobile_number",
        #         "message": ValidationMessages.mobile_number_required.value
        #     }
        #     errors.append(error)
        # else:
        #     user = UserQueryService.getUserByMobileNumber(mobileNumber)
        #     if user:
        #         error = {
        #             "field": "mobile_number",
        #             "message": ValidationMessages.mobile_number_exist.value
        #         }
        #         errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

        # Create user

    def create(self, validated_data):
        userData = {
            'social_type': validated_data.get('social_type', ''),
            'social_id': validated_data.get('social_id', ''),
            'name': validated_data.get('name', ''),
            'mobile_number': validated_data.get('mobile_number', ''),
            'email': validated_data.get('email', ''),
            'password': validated_data.get('password', ''),
            'confirm_password': validated_data.get('confirm_password', '')
        }
        UserQueryService.createUser(userData)
        return validated_data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'mobile_number', 'image']


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'mobile_number']


class UpdatePatientImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'image']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(UpdatePatientImageSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate request data
    def validate(self, data):
        errors = []
        image = data.get('image', None)
        if image == "" or image is None:
            error = {
                "field": "image",
                "message": ValidationMessages.the_profile_image_is_required.value
            }
            errors.append(error)
        else:
            allowedImageFormats = ['jpg', 'png', 'PNG', 'JPEG', 'jpeg']
            fileFormat = str(image).split('.')[-1]
            if fileFormat not in allowedImageFormats:
                error = {
                    "field": "image",
                    "message": ValidationMessages.the_image_format_not_allowed.value
                }
                errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    def update(self, instance, validated_data):
        validated_data['patient_id'] = instance.id
        # Update user password
        UserQueryService.updatePatientUserImage(validated_data)
        return validated_data


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ['email']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(ForgotPasswordSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate request data
    def validate(self, data):
        errors = []
        email = data.get('email', '')
        if email == '' or email is None:
            error = {
                "field": "email",
                "message": ValidationMessages.the_email_field_is_required.value
            }
            errors.append(error)
        else:
            user = UserQueryService.getUserByEmail(email)
            if user is None:
                error = {
                    "field": "email",
                    "message": ValidationMessages.the_email_is_not_valid.value
                }
                errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data


class RestPasswordSerializer(serializers.ModelSerializer):
    forgot_password_otp = serializers.CharField(allow_blank=False)
    new_password = serializers.CharField(allow_blank=False)
    confirm_new_password = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ['forgot_password_otp', 'new_password', 'confirm_new_password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(RestPasswordSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate request data
    def validate(self, data):
        errors = []
        forgot_password_otp = data.get('forgot_password_otp', '')
        new_password = data.get('new_password', '')
        confirm_new_password = data.get('confirm_new_password', '')

        if forgot_password_otp == '' or forgot_password_otp is None:
            error = {
                "field": "forgot_password_otp",
                "message": ValidationMessages.the_forgot_password_otp_field_is_required.value
            }
            errors.append(error)
        else:
            user = UserQueryService.getUserByOtp(forgot_password_otp)
            if user is None:
                error = {
                    "field": "forgot_password_otp",
                    "message": ValidationMessages.the_forgot_password_otp_is_not_valid.value
                }
                errors.append(error)

        if new_password == '' or new_password is None:
            error = {
                "field": "new_password",
                "message": ValidationMessages.the_new_password_field_is_required.value
            }
            errors.append(error)

        if confirm_new_password == '' or confirm_new_password is None:
            error = {
                "field": "confirm_new_password",
                "message": ValidationMessages.the_confirm_password_field_is_required.value
            }
            errors.append(error)

        if new_password != "" or new_password is not None and confirm_new_password != "" or confirm_new_password is not None:
            if new_password != confirm_new_password:
                error = {
                    "field": "confirm_new_password",
                    "message": ValidationMessages.the_confirm_password_and_new_password_must_match.value
                }
                errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Update user password
    def update(self, instance, validated_data):
        userData = {
            'user_id': instance.id,
            'new_password': validated_data.get('new_password'),
            'confirm_password': validated_data.get('confirm_new_password')
        }
        # Update user password
        UserQueryService.updateUserPassword(userData)
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(allow_blank=False)
    new_password = serializers.CharField(allow_blank=False)
    confirm_new_password = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_new_password']

    # Fields Errors Message
    def __init__(self, *args, **kwargs):
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)
        # Override field required and blank message
        MainService.fieldRequiredMessage(self.fields)

    # Validate request data
    def validate(self, data):
        errors = []
        userData = self.context['request'].user
        id = userData.id
        user = UserQueryService.getUserById(id)
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_new_password = data.get('confirm_new_password', '')
        # Validation Errors
        if old_password != '' or old_password is not None:
            if not check_password(old_password, user.password):
                error = {
                    "field": "old_password",
                    "message": ValidationMessages.the_old_password_is_not_correct.value
                }
                errors.append(error)
            else:
                if new_password == '' or new_password is None:
                    error = {
                        "field": "new_password",
                        "message": ValidationMessages.the_new_password_field_is_required.value
                    }
                    errors.append(error)
                elif confirm_new_password == '' or confirm_new_password is None:
                    error = {
                        "field": "new_password",
                        "message": ValidationMessages.the_confirm_password_field_is_required.value
                    }
                    errors.append(error)
                elif new_password != confirm_new_password:
                    error = {
                        "field": "confirm_new_password",
                        "message": ValidationMessages.the_confirm_password_and_new_password_must_match.value
                    }
                    errors.append(error)
        elif old_password == '' or old_password is None:
            error = {
                "field": "old_password",
                "message": ValidationMessages.the_old_password_is_required.value
            }
            errors.append(error)
        if len(errors) > 0:
            raise exceptions.ValidationError(errors)
        return data

    # Update user password
    def update(self, instance, validated_data):
        userData = {
            'user_id': instance.id,
            'new_password': validated_data.get('new_password'),
            'confirm_password': validated_data.get('confirm_new_password')
        }
        # Update user password
        UserQueryService.updateUserPassword(userData)
        return validated_data
