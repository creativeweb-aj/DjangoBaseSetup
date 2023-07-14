import enum
from apps.users.models import User
from django.contrib.sites.shortcuts import get_current_site
import hashlib
from django.shortcuts import render
from DjangoBaseSetup import settings
from apps.settings.models import Setting
import datetime
import time
import os
import random, math, string
from rest_framework_simplejwt.tokens import RefreshToken
from DjangoBaseSetup.messages.messages import MainMessages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password

# Use to get record per page data value form setting model
RECORD_PER_PAGE = 'Reading.records_per_page'

PROTOCOL = 'http://'
RESET_PASSWORD_URL = '/reset-password/'


class Status(enum.Enum):
    success = "SUCCESS"
    fail = "FAIL"
    error = "ERROR"


class RoleType(enum.Enum):
    patient = 2
    doctor = 3
    hospital = 4
    clinic = 5
    pharmacy = 6
    diagnostic = 7


class MainService:
    def __init__(self, request):
        self.request = request
        self.currentSite = get_current_site(self.request)
        self.user = None

    def GenerateOtp(self, user):
        self.user = user
        email = self.user.email
        # Generate otp and pass in method
        digits = '0123456789'
        OTP = ""
        for i in range(0, 6):
            OTP += digits[math.floor(random.random() * 10)]
        user = self.saveOtp(OTP)
        return user

    def forgotPasswordOtp(self, user):
        self.user = user
        email = self.user.email
        timeStamp = time.mktime(datetime.datetime.today().timetuple())
        keyString = str(email) + str(timeStamp)
        res = hashlib.md5(keyString.encode())
        tokenString = res.hexdigest()
        # Generate otp and pass in method
        digits = '0123456789'
        OTP = ""
        for i in range(0, 4):
            OTP += digits[math.floor(random.random() * 10)]
        user = self.saveForgotPasswordData(tokenString, OTP)
        return user

    def saveOtp(self, OTP):
        userObj = User.objects.get(id=self.user.id)
        userObj.forgot_password_otp = OTP
        userObj.save()
        return userObj

    @staticmethod
    def GenerateRandomPswrd(user):
        # Generate otp and pass in method
        symbols = string.ascii_letters + string.digits + string.punctuation
        PSWRD = ""
        for i in range(0, 8):
            PSWRD += random.choice(symbols)
        encryptPSWRD = make_password(PSWRD)
        data = {'encrypted': encryptPSWRD, 'decrypted': PSWRD}
        return data

    def passwordForgotLink(self, user):
        self.user = user
        email = self.user.email
        timeStamp = time.mktime(datetime.datetime.today().timetuple())
        keyString = str(email) + str(timeStamp)
        res = hashlib.md5(keyString.encode())
        tokenString = res.hexdigest()
        user = self.saveForgotPasswordData(tokenString, None)
        return user

    def saveForgotPasswordData(self, tokenString, OTP):
        userObj = User.objects.get(id=self.user.id)
        if OTP is None:
            userObj.forgot_password_string = tokenString
            userObj.save()
        else:
            userObj.forgot_password_string = tokenString
            userObj.forgot_password_otp = OTP
            userObj.save()
        return userObj

    def createUrlString(self, tokenString):
        forgotPasswordUrl = str(self.currentSite) + RESET_PASSWORD_URL + tokenString + '/'
        return forgotPasswordUrl

    @staticmethod
    def getPageRange(results, paginator):
        # Get the index of the current page
        index = results.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so let's calculate where to slice the list
        startIndex = index - 3 if index >= 3 else 0
        endIndex = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns
        # an iterator. Thus pass it to list, to make our slice possible again.
        pageRange = list(paginator.page_range)[startIndex:endIndex]
        return pageRange

    def getPageRecordSize(self):
        recordPerPage = int(settings.READING_RECORD_PER_PAGE)
        # Getting from setting model
        try:
            settingObj = Setting.objects.get(key=RECORD_PER_PAGE)
            if settingObj:
                recordPerPage = int(settingObj.value)
            if self.request.GET.get('page_size') != "" and self.request.GET.get('page_size') is not None:
                recordPerPage = int(self.request.GET.get('page_size'))
        except Setting.DoesNotExist:
            if self.request.GET.get('page_size') != "" and self.request.GET.get('page_size') is not None:
                recordPerPage = int(self.request.GET.get('page_size'))
        return recordPerPage

    @staticmethod
    def saveMediaFile(fileObj, dirPath, uploadPath):
        # Create folder
        day = str(datetime.datetime.now().day)
        month = str(datetime.datetime.now().month)
        year = str(datetime.datetime.now().year)
        dateTime = day + '-' + month + '-' + year
        folder = dirPath + dateTime + "/"
        folderDirectory = uploadPath + dateTime + "/"
        if not os.path.exists(folder):
            os.mkdir(folder)
        # Save file
        try:
            fs = FileSystemStorage()
            fileName = fileObj.name.split(".")[0].lower()
            fileName = fileName.replace(' ', '')
            extension = fileObj.name.split(".")[-1].lower()
            timeStamp = str(int(datetime.datetime.now().timestamp()))
            newFileName = fileName + '-' + timeStamp + "." + extension
            fs.save(folderDirectory + newFileName, fileObj)
            imageUrl = '/' + dirPath + dateTime + '/' + newFileName
        except FileNotFoundError:
            print(f'Exception ==> {FileNotFoundError}')
            imageUrl = ''
        return imageUrl

    @staticmethod
    def deleteMediaFile(fileUrl, dirPath):
        # delete file
        try:
            file_name = fileUrl.split('/')[-1]
            dir_name = fileUrl.split('/')[-2]
            os.remove(os.path.join(dirPath + dir_name, file_name))
        except FileNotFoundError:
            print(f'Exception ==> {FileNotFoundError}')
        return "Delete"

    @staticmethod
    def getJwtToken(typeName, user):
        refresh = RefreshToken.for_user(user)
        data = {}
        if typeName == 'ACCESS_TOKEN':
            data['access_token'] = str(refresh.access_token)
        else:
            data['refresh_token'] = str(refresh)
        return data

    @staticmethod
    def fieldRequiredMessage(fields):
        for field in fields:
            fields[field].error_messages["required"] = MainMessages.the.value + ' ' + \
                                                       field.replace('_', ' ') + ' ' + \
                                                       MainMessages.field_is_required.value.lower()

            fields[field].error_messages["blank"] = MainMessages.the.value + ' ' + \
                                                    field.replace('_', ' ') + ' ' + \
                                                    MainMessages.field_is_required.value.lower()

    @staticmethod
    def error_404(request, exception):
        data = {}
        return render(request, 'errors/404.html', data)

    @staticmethod
    def error_500(request, *args, **argv):
        return render(request, 'errors/500.html', status=500)

    @staticmethod
    def error_400(request, *args, **argv):
        return render(request, 'errors/400.html', status=400)

    @staticmethod
    def error_403(request, *args, **argv):
        return render(request, 'errors/403.html', status=403)

    @staticmethod
    def CreateUser(data, role: int, isAdd: bool, userId=None):
        if isAdd:
            userObj = User()
            userObj.user_role_id = int(role)
            userObj.email = data.get('email', None)
            userObj.first_name = data.get('first_name', None)
            userObj.last_name = data.get('last_name', None)
            userObj.mobile_number = data.get('mobile_number', None)
            userObj.password = make_password(data.get('password', None))
            userObj.confirm_password = make_password(data.get('confirm_password', None))
            userObj.image = data.get('image', None)
            userObj.address1 = data.get('address1', None)
            userObj.address2 = data.get('address2', None)
            userObj.city = data.get('city', None)
            userObj.country = data.get('country', None)
            userObj.state = data.get('state', None)
            userObj.zip_code = data.get('zip_code', None)
            userObj.save()
        else:
            userObj = User.objects.filter(id=int(userId), user_role_id=role).first()
            if userObj:
                userObj.email = data.get('email', None)
                userObj.mobile_number = data.get('mobile_number', None)
                userObj.first_name = data.get('first_name', None)
                userObj.last_name = data.get('last_name', None)
                if data.get('image', None):
                    userObj.image = data.get('image', None)
                userObj.address1 = data.get('address1', None)
                userObj.address2 = data.get('address2', None)
                userObj.city = data.get('city', None)
                userObj.country = data.get('country', None)
                userObj.state = data.get('state', None)
                userObj.zip_code = data.get('zip_code', None)
                userObj.save()

        return userObj

    @staticmethod
    def daysList():
        days = ["ALL", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
        # ('ALL', 'All'),
        # ('SUN', 'Sun'),
        # ('MON', 'Mon'),
        # ('TUE', 'Tue'),
        # ('WED', 'Wed'),
        # ('THUR', 'Thur'),
        # ('FIR', 'Fir'),
        # ('SAT', 'Sat')
        # ]
        return days

    @staticmethod
    def getDefaultImages(imageType: str):
        image = None
        if imageType == "UserApi":
            settingObj = Setting.objects.filter(key="Site.user_image").first()
            image = settingObj.value
        elif imageType == "hospital":
            settingObj = Setting.objects.filter(key="Site.hospital_image").first()
            image = settingObj.value
        elif imageType == "doctor_aadhar_card":
            settingObj = Setting.objects.filter(key="Site.doctor_aadhar_card").first()
            image = settingObj.value
        elif imageType == "doctor_mci_cert":
            settingObj = Setting.objects.filter(key="Site.doctor_mci_cert").first()
            image = settingObj.value
        if image:
            image = str(settings.BASE_URL) + str(image)
        return image
