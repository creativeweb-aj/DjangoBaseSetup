from DjangoBaseSetup.common_modules.mainService import Status
from DjangoBaseSetup.messages.messages import (ApiResponseMessage,
                                           LoginMessages)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from apps.api.modules.user.UserSerializer import MobileLoginSerializer, VerifyMobileLoginSerializer, \
    ResendOtpSerializer, SocialLoginSerializer, PatientSerializer, UpdatePatientSerializer, \
    AddPatientSerializer, UpdatePatientImageSerializer
from .UserService import UserQueryService
from apps.api.modules import responseData, setException


# Create your views here.
@swagger_auto_schema(
    method='post',
    request_body=SocialLoginSerializer,
    responses=responseData
)
@api_view(['POST'])
def socialLogin(request):
    resData = dict()
    # Initialize user serializer to validate data
    serializer = SocialLoginSerializer(data=request.data)
    if serializer.is_valid():
        socialId = serializer.data.get('social_id', None)
        print(f"socialId --> {socialId}")
        user = UserQueryService.getUserBySocialId(socialId)
        print(f"user --> {user}")
        if user:
            # Get Access Token
            token = MainService.getJwtToken('ACCESS_TOKEN', user)
            patient = UserQueryService.getParentPatientByUserId(user.id)
            print(f"patient --> {patient}")
            patientSerializer = PatientSerializer(instance=patient)
            # Make response data success case
            resData['status'] = Status.success.value
            resData['data'] = {"token": token, "user": patientSerializer.data, "role_id": user.user_role_id}
            resData['message'] = LoginMessages.you_are_now_logged_in.value
            resData['errors'] = []
            status_code = 200
            return Response(resData, status=status_code)
        email = serializer.data.get('email', None)
        user = UserQueryService.getUserByEmail(email)
        print(f"user email --> {user}")
        if user:
            # Get Access Token
            token = MainService.getJwtToken('ACCESS_TOKEN', user)
            patient = UserQueryService.getParentPatientByUserId(user.id)
            patientSerializer = PatientSerializer(instance=patient)
            # Make response data success case
            resData['status'] = Status.success.value
            resData['data'] = {"token": token, "user": patientSerializer.data, "role_id": user.user_role_id}
            resData['message'] = LoginMessages.you_are_now_logged_in.value
            resData['errors'] = []
            status_code = 200
            return Response(resData, status=status_code)
        # mobileNumber = serializer.data.get('mobile_number', None)
        # user = UserQueryService.getUserByMobileNumber(mobileNumber)
        # print(f"user mobileNumber --> {user}")
        # if user:
        #     # Get Access Token
        #     token = MainService.getJwtToken('ACCESS_TOKEN', user)
        #     patient = UserQueryService.getParentPatientByUserId(user.id)
        #     patientSerializer = PatientSerializer(instance=patient)
        #     # Make response data success case
        #     resData['status'] = 'SUCCESS'
        #     resData['data'] = {"token": token, "user": patientSerializer.data, "role_id": user.user_role_id}
        #     resData['message'] = LoginMessages.you_are_now_logged_in.value
        #     resData['errors'] = []
        #     status_code = 200
        #     return Response(resData, status=status_code)
        user = UserQueryService.createUser(serializer.data)
        print(f"user createUser --> {user}")
        if user:
            # Get Access Token
            token = MainService.getJwtToken('ACCESS_TOKEN', user)
            patient = UserQueryService.getParentPatientByUserId(user.id)
            patientSerializer = PatientSerializer(instance=patient)
            # Make response data success case
            resData['status'] = Status.success.value
            resData['data'] = {"token": token, "user": patientSerializer.data, "role_id": user.user_role_id}
            resData['message'] = LoginMessages.you_are_now_logged_in.value
            resData['errors'] = []
            status_code = 200
            return Response(resData, status=status_code)
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
        return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=MobileLoginSerializer,
    responses=responseData
)
@api_view(['POST'])
def mobileLogin(request):
    resData = dict()
    # Initialize user serializer to validate data
    serializer = MobileLoginSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = UserQueryService.getUserByMobileNumber(serializer.data.get('mobile_number', None))
        # Make response data fail case
        resData['status'] = Status.success.value
        resData['data'] = {'user_id': user.id}
        resData['message'] = LoginMessages.otp_sent_to_mobile.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=ResendOtpSerializer,
    responses=responseData
)
@api_view(['POST'])
def resendOtp(request):
    resData = dict()
    # Initialize user serializer to validate data
    serializer = ResendOtpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Make response data fail case
        resData['status'] = Status.success.value
        resData['data'] = None
        resData['message'] = LoginMessages.otp_sent_to_mobile.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=VerifyMobileLoginSerializer,
    responses=responseData
)
@api_view(['POST'])
def verifyMobileLogin(request):
    resData = dict()
    # Initialize user serializer to validate data
    serializer = VerifyMobileLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = UserQueryService.getUserById(serializer.data.get('user_id', None))
        if user:
            user.mobile_otp = None
            user.save()
        token = MainService.getJwtToken('ACCESS_TOKEN', user)
        # Serialize user data and pass
        patient = UserQueryService.getParentPatientByUserId(serializer.data.get('user_id', None))
        patientSerializer = PatientSerializer(instance=patient)
        # Make response data fail case
        resData['status'] = Status.success.value
        resData['data'] = {"token": token, "user": patientSerializer.data, "role_id": user.user_role_id}
        resData['message'] = ApiResponseMessage.userLoginSuccess.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)


# @swagger_auto_schema(
#     method='post',
#     request_body=ForgotPasswordSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# def forgotPassword(request):
#     resData = dict()
#     serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid():
#         email = serializer.data['email']
#         user = UserQuery.getUserByEmail(email)
#         # Create password forgot url and save in db
#         service = MainService(request)
#         user = service.forgotPasswordOtp(user)
#         # Send email to user
#         EmailService(request, user, EmailType.forgotPasswordOtp.value)
#         # Make response data success case
#         resData['status'] = 'success'
#         resData['data'] = {}
#         resData['message'] = ApiResponseMessage.emailSent.value
#         resData['errors'] = []
#         status_code = 200
#     else:
#         # Make response data fail case
#         res = setException(serializer)
#         resData['status'] = 'error'
#         resData['data'] = {}
#         resData['message'] = res.get('message')
#         resData['errors'] = res.get('errors')
#         status_code = 200
#     return Response(resData, status=status_code)
#
#
# @swagger_auto_schema(
#     method='post',
#     request_body=RestPasswordSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# def resetPassword(request):
#     resData = dict()
#     otp = request.data.get('forgot_password_otp', None)
#     user = UserQuery.getUserByOtp(otp)
#     serializer = RestPasswordSerializer(data=request.data, instance=user, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         # Make response data success case
#         resData['status'] = 'success'
#         resData['data'] = {}
#         resData['message'] = ApiResponseMessage.passwordResetSuccess.value
#         resData['errors'] = []
#         status_code = 200
#     else:
#         # Make response data fail case
#         res = setException(serializer)
#         resData['status'] = 'error'
#         resData['data'] = {}
#         resData['message'] = res.get('message')
#         resData['errors'] = res.get('errors')
#         status_code = 200
#     return Response(resData, status=status_code)
#
#
# @swagger_auto_schema(
#     method='post',
#     request_body=ChangePasswordSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def changePassword(request):
#     resData = dict()
#     user = UserQuery.getUserById(request.user.id)
#     serializer = ChangePasswordSerializer(data=request.data, instance=user, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         # Make response data success case
#         resData['status'] = 'success'
#         resData['data'] = {}
#         resData['message'] = ApiResponseMessage.passwordChangedSuccess.value
#         resData['errors'] = []
#         status_code = 200
#     else:
#         # Make response data fail case
#         res = setException(serializer)
#         resData['status'] = 'error'
#         resData['data'] = {}
#         resData['message'] = res.get('message')
#         resData['errors'] = res.get('errors')
#         status_code = 200
#     return Response(resData, status=status_code)


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def userProfile(request):
    resData = dict()
    patient = UserQueryService.getParentPatientByUserId(request.user.id)
    patientParentSerializer = PatientSerializer(instance=patient)
    patients = UserQueryService.getChildPatientByUserId(request.user.id)
    patientChildSerializer = PatientSerializer(instance=patients, many=True)
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {"user": patientParentSerializer.data, "profiles": patientChildSerializer.data}
    resData['message'] = ApiResponseMessage.dataSentSuccess.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=UpdatePatientSerializer,
    responses=responseData
)
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    resData = dict()
    patient = UserQueryService.getParentPatientByUserId(request.user.id)
    serializer = UpdatePatientSerializer(data=request.data, instance=patient, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        patient = UserQueryService.getParentPatientByUserId(request.user.id)
        patientSerializer = PatientSerializer(instance=patient)
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = {"user": patientSerializer.data}
        resData['message'] = ApiResponseMessage.userEditProfile.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def myProfiles(request):
    resData = dict()
    patients = UserQueryService.getChildPatientByUserId(request.user.id)
    patientSerializer = PatientSerializer(instance=patients, many=True)
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {"profiles": patientSerializer.data}
    resData['message'] = ApiResponseMessage.dataSentSuccess.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=AddPatientSerializer,
    responses=responseData
)
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def addProfile(request):
    resData = dict()
    serializer = AddPatientSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = serializer.data
        resData['message'] = ApiResponseMessage.profileAdded.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def childProfile(request, Id):
    resData = dict()
    patient = UserQueryService.getChildPatientById(Id)
    patientSerializer = PatientSerializer(instance=patient)
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {"profile": patientSerializer.data}
    resData['message'] = ApiResponseMessage.dataSentSuccess.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=UpdatePatientSerializer,
    responses=responseData
)
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateChildProfile(request, Id):
    resData = dict()
    patient = UserQueryService.getChildPatientById(Id)
    serializer = UpdatePatientSerializer(data=request.data, instance=patient, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        patient = UserQueryService.getChildPatientById(Id)
        patientSerializer = PatientSerializer(instance=patient)
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = {"profile": patientSerializer.data}
        resData['message'] = ApiResponseMessage.profile_updated_successfully.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def deleteChildProfile(request, Id):
    resData = dict()
    patient = UserQueryService.getChildPatientById(Id)
    if patient:
        patient.is_delete = True
        patient.save()
        message = ApiResponseMessage.profile_deleted_successfully.value
        status = Status.success.value
    else:
        message = ApiResponseMessage.profile_not_found.value
        status = Status.fail.value
    # Make response data success case
    resData['status'] = status
    resData['data'] = None
    resData['message'] = message
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=UpdatePatientImageSerializer,
    responses=responseData
)
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateProfileImage(request):
    resData = dict()
    patient = UserQueryService.getParentPatientByUserId(request.user.id)
    serializer = UpdatePatientImageSerializer(data=request.data, instance=patient, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        patient = UserQueryService.getParentPatientByUserId(request.user.id)
        patientSerializer = PatientSerializer(instance=patient)
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = patientSerializer.data
        resData['message'] = ApiResponseMessage.userEditProfileImage.value
        resData['errors'] = []
        status_code = 200
    else:
        # Make response data fail case
        res = setException(serializer)
        resData['status'] = Status.error.value
        resData['data'] = {}
        resData['message'] = res.get('message')
        resData['errors'] = res.get('errors')
        status_code = 200
    return Response(resData, status=status_code)
