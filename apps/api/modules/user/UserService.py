import datetime
import random
import math
import pytz
import string
from django.contrib.auth.hashers import make_password
from apps.api.modules.master.MasterService import MasterService
from apps.patient_management.models import Patient
from apps.users.models import User


class UserQueryService:
    def __init__(self):
        pass

    # Get user data by email id
    @staticmethod
    def getUserByEmail(email: str) -> any:
        try:
            user = User.objects.get(email=email, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    @staticmethod
    def getUserByEmailCheckAll(email: str) -> any:
        try:
            user = User.objects.get(email=email, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Get user data by email id
    @staticmethod
    def getUserBySocialId(socialId: str) -> any:
        try:
            user = User.objects.get(social_id=socialId, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Get user data by email id
    @staticmethod
    def getUserByOtp(otp: str) -> any:
        try:
            user = User.objects.get(forgot_password_otp=otp, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Check user exist or not by mobile number
    @staticmethod
    def getUserByMobileNumber(number: int) -> any:
        try:
            user = User.objects.get(mobile_number=number, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    # Get user by user id
    @staticmethod
    def getUserById(userId: int) -> any:
        try:
            user = User.objects.get(id=userId, user_role_id=2, is_active=True, is_delete=False)
        except Exception as e:
            user = None
        return user

    @staticmethod
    def getParentPatientByUserId(userId: int) -> any:
        try:
            patient = Patient.objects.get(user_id__id=userId, is_parent=True, is_active=True, is_delete=False)
        except Exception as e:
            patient = None
        return patient

    @staticmethod
    def getChildPatientByUserId(userId: int) -> any:
        try:
            patient = Patient.objects.get(user_id__id=userId, is_parent=True, is_active=True, is_delete=False)
            if patient:
                patientObj = Patient.objects.filter(user_id__id=userId, parent_id=patient, is_parent=False,
                                                    is_active=True, is_delete=False)
            else:
                patientObj = None
        except Exception as e:
            patientObj = None
        return patientObj

    @staticmethod
    def getChildPatientById(Id: int) -> any:
        try:
            patient = Patient.objects.filter(id=Id, is_parent=False,
                                             is_active=True, is_delete=False).first()
        except Exception as e:
            patient = None
        return patient

    @staticmethod
    def checkOtpExpireById(userId: int) -> any:
        currDateTime = datetime.datetime.now(pytz.timezone('UTC'))
        print(f"currDateTime --> {currDateTime}")
        try:
            user = User.objects.filter(
                id=userId,
                otp_expired_in__gte=currDateTime,
                user_role_id=2,
                is_active=True,
                is_delete=False
            ).first()
            print(f"user --> {user.otp_expired_in}")
        except Exception as e:
            user = None
        return user

    # Create user or save user data
    @classmethod
    def createUser(cls, data: dict) -> any:
        print(f"data --> {data}")
        user = cls.getUserByEmail(data.get('email', None))
        if user:
            try:
                name = data.get('name', '')
                try:
                    firstName = name.split(' ')[0]
                except Exception as e:
                    firstName = None
                try:
                    lastName = name.split(' ')[1]
                except Exception as e:
                    lastName = None
                user.first_name = firstName
                user.last_name = lastName
                user.mobile_number = data.get('mobile_number', None)
                user.email = data.get('email', '')
                user.password = make_password(data.get('password', ''))
                user.confirm_password = data.get('confirm_password', '')
                user.social_type = data.get('social_type', None)
                user.social_id = data.get('social_id', None)
                user.save()
                cls.addUpdatePatient(user)
            except Exception as e:
                print(f"e --> {e}")
                user = None
        else:
            try:
                user = User()
                name = data.get('name', '')
                try:
                    firstName = name.split(' ')[0]
                except Exception as e:
                    firstName = None
                try:
                    lastName = name.split(' ')[1]
                except Exception as e:
                    lastName = None
                user.first_name = firstName
                user.last_name = lastName
                user.user_role_id = 2
                user.mobile_number = data.get('mobile_number', None)
                user.email = data.get('email', '')
                user.password = make_password(data.get('password', ''))
                user.confirm_password = data.get('confirm_password', '')
                user.social_type = data.get('social_type', None)
                user.social_id = data.get('social_id', None)
                user.save()
                cls.addUpdatePatient(user)
            except Exception as e:
                print(f"e --> {e}")
                user = None
        return user

    # Update user password
    @classmethod
    def updateUserPassword(cls, data: dict) -> any:
        try:
            user = cls.getUserById(data['user_id'])
            user.forgot_password_otp = None
            user.password = make_password(data['new_password'])
            user.confirm_password = data['confirm_password']
            user.save()
        except Exception as e:
            user = None
        return user

    @staticmethod
    def addUpdatePatient(user: any) -> any:
        try:
            name = ''
            if user.first_name:
                name += user.first_name
            if user.last_name:
                name += ' ' + user.last_name
            patient = Patient.objects.filter(user_id=user).first()
            if patient:
                patient.full_name = name
                patient.email = user.email
                patient.mobile_number = user.mobile_number
                patient.save()
            else:
                mrdStr = '#'+''.join(random.sample(string.ascii_uppercase + string.digits, 15))
                patient = Patient()
                patient.user_id = user
                patient.full_name = name
                patient.email = user.email
                patient.mobile_number = user.mobile_number
                patient.mrd_no = mrdStr
                patient.is_parent = True
                patient.save()
            return patient
        except Exception as e:
            print(f"Exception (addUpdatePatient) -> {e}")
            return None

    @classmethod
    def updatePatientUserProfile(cls, data: any) -> any:
        try:
            patient = Patient.objects.filter(id=data.get('patient_id', None)).first()
            print(f"patient --> {patient.is_parent}")
            if patient:
                if patient.is_parent:
                    patient.full_name = data.get('full_name', None)
                    patient.email = data.get('email', None)
                    patient.mobile_number = data.get('mobile_number', None)
                    patient.gender = data.get('gender', None)
                    patient.dob = data.get('dob', None)
                    patient.address = data.get('address', None)
                    if data.get('image', None):
                        patient.image = data.get('image', None)
                    patient.latitude = data.get('latitude', None)
                    patient.longitude = data.get('longitude', None)
                    patient.save()
                    # Update user model also when it's parent patient
                    cls.updateParentPatientUserProfile(patient)
                else:
                    if data.get('relationship', None):
                        relationshipType = MasterService.getRelationshipById(int(data.get('relationship', None)))
                    else:
                        relationshipType = None
                    patient.full_name = data.get('full_name', None)
                    patient.email = data.get('email', None)
                    patient.mobile_number = data.get('mobile_number', None)
                    patient.gender = data.get('gender', None)
                    patient.dob = data.get('dob', None)
                    patient.address = data.get('address', None)
                    if relationshipType:
                        patient.relationship = relationshipType
                    if data.get('image', None):
                        patient.image = data.get('image', None)
                    patient.latitude = data.get('latitude', None)
                    patient.longitude = data.get('longitude', None)
                    patient.save()
            return patient
        except Exception as e:
            print(f"Exception (updatePatientUserProfile) -> {e}")
            return None

    @staticmethod
    def updatePatientUserImage(data: dict) -> any:
        try:
            patient = Patient.objects.filter(id=data.get('patient_id', None)).first()
            if patient:
                patient.image = data.get('image', None)
                patient.save()
            return patient
        except Exception as e:
            print(f"Exception (addUpdatePatient) -> {e}")
            return None

    @classmethod
    def addPatientUserProfile(cls, data: any) -> any:
        try:
            mrdStr = '#'+''.join(random.sample(string.ascii_uppercase + string.digits, 15))
            user = data.get('user', None)
            relationshipType = MasterService.getRelationshipById(int(data.get('relationship', None)))
            patientObj = cls.getParentPatientByUserId(user.id)
            patient = Patient()
            patient.user_id = user
            patient.mrd_no = mrdStr
            patient.parent_id = patientObj
            patient.full_name = data.get('full_name', None)
            patient.email = data.get('email', None)
            patient.mobile_number = data.get('mobile_number', None)
            patient.gender = data.get('gender', None)
            patient.dob = data.get('dob', None)
            patient.image = data.get('image', None)
            patient.address = data.get('address', None)
            patient.relationship = relationshipType
            patient.latitude = data.get('latitude', None)
            patient.longitude = data.get('longitude', None)
            patient.is_parent = False
            patient.save()
            return patient
        except Exception as e:
            print(f"Exception (addUpdatePatient) -> {e}")
            return None

    @classmethod
    def createUpdateUserMobileLogin(cls, data: dict) -> any:
        try:
            print(f"data --> {data}")
            otpData = cls.generateMobileOtp(cls)
            print(f"otpData --> {otpData}")
            email = str(data.get('mobile_number', otpData.get('OTP', ''))) + '@mobile.com'
            user = cls.getUserByMobileNumber(data.get('mobile_number', None))
            if user:
                user.mobile_otp = otpData.get('OTP', None)
                user.otp_expired_in = otpData.get('date', None)
                user.save()
            else:
                user = User()
                user.user_role_id = 2
                user.email = email
                user.mobile_number = data.get('mobile_number', None)
                user.mobile_otp = otpData.get('OTP', None)
                user.otp_expired_in = otpData.get('date', None)
                user.save()
            cls.addUpdatePatient(user)
        except Exception as e:
            print(f"Exception: createUserMobileLogin {e}")
            user = None
        return user

    @classmethod
    def updateUserMobileOtp(cls, data: dict) -> any:
        try:
            otpData = cls.generateMobileOtp(cls)
            user = cls.getUserById(data.get('user_id', None))
            if user:
                user.mobile_otp = otpData.get('OTP', None)
                user.otp_expired_in = otpData.get('date', None)
                user.save()
        except Exception as e:
            print(f"Exception: createUserMobileLogin {e}")
            user = None
        return user

    @staticmethod
    def generateMobileOtp(cls) -> dict:
        date = datetime.datetime.now()
        otpSec = 30
        date = date + datetime.timedelta(seconds=otpSec)
        digits = [i for i in range(0, 10)]
        OTP = ''
        for i in range(6):
            index = math.floor(random.random() * 10)
            OTP += str(digits[index])
        OTP = int(OTP)
        OTP = 123456  # Comment after sms servie start
        cls.sendToMobile(OTP)
        data = {
            "OTP": OTP,
            "date": date
        }
        return data

    @staticmethod
    def updateParentPatientUserProfile(patient):
        print(f"patient --> {dir(patient)}")
        user = User.objects.filter(id=patient.user_id.id, user_role_id=2, is_active=True, is_delete=False).first()
        print(f"user --> {dir(user)}")
        if user:
            try:
                firstName = patient.full_name.split(' ')[0]
            except Exception as e:
                firstName = None
            try:
                lastName = patient.full_name.split(' ')[1]
            except Exception as e:
                lastName = None
            try:
                user.first_name = firstName
                user.last_name = lastName
                user.email = patient.email
                user.mobile_number = patient.mobile_number
                user.image = patient.image
                user.save()
            except Exception as e:
                print(f"updateParentPatientUserProfile user --> {e}")
            return user
        else:
            return None

    @staticmethod
    def sendToMobile(OTP: int) -> any:
        pass
