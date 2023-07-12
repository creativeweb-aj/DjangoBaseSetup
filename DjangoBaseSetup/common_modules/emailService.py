import re
import enum
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from apps.email_logs.models import EmailLog
from apps.users.models import User
from apps.email_templates.models import EmailActions, EmailTemplates
from apps.settings.models import Setting
from DjangoBaseSetup.common_modules.mainService import MainService

# Global variable
RESET_PASSWORD_URL = '/reset-password/'
EMAIL_HOST_USER = 'Site.EmailFrom'


class EmailType(enum.Enum):
    passwordReset = 'PASSWORD_RESET_DONE'
    loginCredentials = 'SEND_LOGIN_CREDENTIALS'
    forgotPassword = 'FORGOT_PASSWORD'
    forgotPasswordOtp = 'FORGOT_PASSWORD_OTP'
    VerifyUserOtp = 'Verify_User_OTP'
    changeEmailOtp = 'NEW_EMAIL_OTP'
    signupOtp = 'FORGOT_PASSWORD_OTP'


# Email Sending Service
class EmailService:
    def __init__(self, request, user, emailType):
        # Initialize all variables
        self.user = user
        self.request = request
        self.emailType = emailType
        self.emailFrom = None
        self.subject = None
        self.messageBody = None
        if emailType == 'NEW_EMAIL_OTP':
            self.newEmail = request.data['new_email']
        # Get and set email host
        self.getEmailHost()
        # get email objects data from model
        data = self.getEmailObject()
        if data:
            self.objData = data
        else:
            self.objData = None
        # Create email contents to send email
        isReady = self.generateEmailContent()
        if isReady:  # Content is ready
            # Email send
            self.sendEmail()
        else:  # Content is not ready
            print('Email Not Sent Content Not Ready')

    # Email Host Name
    def getEmailHost(self):
        self.emailFrom = settings.EMAIL_HOST_USER
        try:
            obj = Setting.objects.filter(key=EMAIL_HOST_USER).first()
            if obj is not None:
                self.emailFrom = obj.value
        except:
            pass
        return True

    # Get data from email templates
    def getEmailObject(self):
        if self.emailType is not None:
            emailActions = EmailActions.objects.filter(action=self.emailType).first()
            if emailActions:
                emailTemplate = EmailTemplates.objects.filter(action=emailActions.id).first()
            else:
                emailTemplate = None
        else:
            emailActions = None
            emailTemplate = None
        data = dict()
        if emailActions is not None:
            data['emailActions'] = emailActions
        if emailTemplate is not None:
            data['emailTemplate'] = emailTemplate
        return data

    # Make email data
    def generateEmailContent(self):
        if self.objData is not None:
            # Create constant list
            constants = list()
            options = (self.objData['emailActions'].option.split(','))
            for const in options:
                constants.append("{" + const + "}")
            # Get subject and body from email template object
            self.subject = self.objData['emailTemplate'].subject

            self.messageBody = self.objData['emailTemplate'].body
            # Create constant values according to email type
            constantValues = self.createConstantValueList()
            # Start constants loop and replace constant by it values
            for i in range(len(constants)):
                self.messageBody = re.sub(
                    constants[i],
                    constantValues[i],
                    self.messageBody
                )
            self.messageBody = re.sub(r'&nbsp;', ' ', self.messageBody, flags=re.IGNORECASE)
            return True
        else:
            print("Error Content Not Create Object None")
            return False

    # Create constants values list
    def createConstantValueList(self):
        constantValues = list()
        if self.emailType == EmailType.loginCredentials.value:
            passwordData = MainService.GenerateRandomPswrd(self.user)
            userObj = User.objects.filter(id=self.user.id).first()

            userObj.password = userObj.confirm_password = passwordData['encrypted']
            userObj.save()
            if userObj.user_role_id == 2:
                constantValues = [
                    self.user.first_name,
                    self.user.email,
                    passwordData['decrypted']
                ]
            else:
                constantValues = [
                    self.user.first_name,
                    self.user.email,
                    passwordData['decrypted']
                ]
        elif self.emailType == EmailType.forgotPassword.value:
            tokenString = self.user.forgot_password_string
            service = MainService(self.request)
            forgotPasswordUrl = service.createUrlString(tokenString)
            constantValues = [forgotPasswordUrl]
        elif self.emailType == EmailType.forgotPasswordOtp.value:
            otp = self.user.forgot_password_otp
            constantValues = [otp]
        elif self.emailType == EmailType.VerifyUserOtp.value:
            otp = self.user.forgot_password_otp
            constantValues = [otp]
        elif self.emailType == EmailType.passwordReset.value:
            if self.user.first_name and self.user.last_name:
                constantValues = [
                    self.user.first_name + ' ' + self.user.last_name,
                ]
            else:
                constantValues = [
                    self.user.email
                ]

        elif self.emailType == EmailType.changeEmailOtp.value:
            otp = self.user.forgot_password_otp
            constantValues = [otp]
        return constantValues

    # Email Send Method
    def sendEmail(self):
        try:
            if self.emailType == 'NEW_EMAIL_OTP':
                emailData = EmailMultiAlternatives(self.subject, self.messageBody, to=[self.newEmail])
            else:
                emailData = EmailMultiAlternatives(self.subject, self.messageBody, to=[self.user.email])
            emailData.content_subtype = "html"
            try:
                emailData.send()
            except Exception as e:
                print("Email not sent in send ==> ", e)
            # Save email logs
            self.saveEmailLogs()
        except Exception as e:
            print("Email not sent ==> ", e)

    # Save email logs method
    def saveEmailLogs(self):
        emailLog = EmailLog()
        emailLog.email_from = self.emailFrom
        if self.emailType == 'NEW_EMAIL_OTP':
            emailLog.email_to = self.newEmail
        else:
            emailLog.email_to = self.user.email
        emailLog.subject = self.subject
        emailLog.message = self.messageBody
        emailLog.save()
        return True
