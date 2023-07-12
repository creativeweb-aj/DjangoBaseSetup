# from DjangoBaseSetup.common_modules.emailService import EmailService, EmailType
# from DjangoBaseSetup.common_modules.mainService import MainService
# from DjangoBaseSetup.messages.messages import (ApiResponseMessage,
#                                            LoginMessages)
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.decorators import (api_view, authentication_classes,
#                                        permission_classes)
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.decorators import parser_classes
# from rest_framework.parsers import FormParser, MultiPartParser
# from apps.api.query import UserQuery
#
# # Response Body Default Schema
# pageParam = openapi.Parameter(
#     'page',
#     openapi.IN_QUERY,
#     description="Send page number in query param",
#     type=openapi.TYPE_STRING
# )
# responseData = {
#     200: openapi.Schema(
#         type=openapi.TYPE_STRING,
#         status="SUCCESS",
#         data=openapi.TYPE_OBJECT,
#         message=openapi.TYPE_STRING
#     ),
#     400: openapi.Schema(
#         type=openapi.TYPE_STRING,
#         status="FAIL",
#         data=openapi.TYPE_OBJECT,
#         message=openapi.TYPE_STRING
#     )
# }
#
#
# # Set error messages from serializer
# def setException(serializer):
#     errors = []
#     message = ''
#     for error in serializer.errors:
#         if error == "non_field_errors":
#             data = serializer.errors[error][0]
#             errors.append(data)
#             message = addString(message, serializer.errors[error][0])
#         else:
#             data = {
#                 "field": error,
#                 "message": serializer.errors[error][0]
#             }
#             errors.append(data)
#             message = addString(message, serializer.errors[error][0])
#
#     res = {
#         "errors": errors,
#         "message": message
#     }
#     return res
#
#
# def addString(string, value):
#     if string:
#         if type(value) == dict:
#             string = string + ', ' + value.get('message')
#         else:
#             string = string + ', ' + value
#     else:
#         if type(value) == dict:
#             string = value.get('message')
#         else:
#             string = value
#     return string
#
#
# # Create your views here.
# @swagger_auto_schema(
#     method='post',
#     request_body=SocialLoginSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# def socialLogin(request):
#     resData = dict()
#     # Initialize user serializer to validate data
#     serializer = SocialLoginSerializer(data=request.data)
#     if serializer.is_valid():
#         socialId = serializer.data['social_id']
#         user = UserQuery.getUserBySocialId(socialId)
#         if user:
#             # Get Access Token
#             token = MainService.getJwtToken('ACCESS_TOKEN', user)
#             # Make response data success case
#             resData['status'] = 'success'
#             resData['data'] = token
#             resData['message'] = LoginMessages.you_are_now_logged_in.value
#             resData['errors'] = []
#             status_code = 200
#             return Response(resData, status=status_code)
#
#         email = serializer.data.get('email', '')
#         user = UserQuery.getUserByEmail(email)
#         if user:
#             # Get Access Token
#             token = MainService.getJwtToken('ACCESS_TOKEN', user)
#             # Make response data success case
#             resData['status'] = 'success'
#             resData['data'] = token
#             resData['message'] = LoginMessages.you_are_now_logged_in.value
#             resData['errors'] = []
#             status_code = 200
#             return Response(resData, status=status_code)
#
#         mobileNumber = serializer.data.get('mobile_number', '')
#         user = UserQuery.getUserByMobileNumber(mobileNumber)
#         if user:
#             # Get Access Token
#             token = MainService.getJwtToken('ACCESS_TOKEN', user)
#             # Make response data success case
#             resData['status'] = 'success'
#             resData['data'] = token
#             resData['message'] = LoginMessages.you_are_now_logged_in.value
#             resData['errors'] = []
#             status_code = 200
#             return Response(resData, status=status_code)
#
#         user = UserQuery.createUser(serializer.data)
#         if user:
#             # Get Access Token
#             token = MainService.getJwtToken('ACCESS_TOKEN', user)
#             # Make response data success case
#             resData['status'] = 'success'
#             resData['data'] = token
#             resData['message'] = LoginMessages.you_are_now_logged_in.value
#             resData['errors'] = []
#             status_code = 200
#             return Response(resData, status=status_code)
#     else:
#         # Make response data fail case
#         res = setException(serializer)
#         resData['status'] = 'error'
#         resData['data'] = {}
#         resData['message'] = res.get('message')
#         resData['errors'] = res.get('errors')
#         status_code = 200
#         return Response(resData, status=status_code)
#
#
# # Create your views here.
# # @swagger_auto_schema(
# #     method='post',
# #     request_body=CreateUserSerializer,
# #     responses=responseData
# # )
# # @api_view(['POST'])
# # def register(request):
# #     resData = dict()
# #     # Initialize user serializer to validate data and create user
# #     serializer = CreateUserSerializer(data=request.data)
# #     if serializer.is_valid():
# #         serializer.save()
# #         email = serializer.data['email']
# #         user = UserQuery.getUserByEmail(email)
# #         # Email Sending Service Called
# #         EmailService(request, user, EmailType.register.value)
# #         # Get Access Token
# #         token = MainService.getJwtToken('ACCESS_TOKEN', user)
# #         # Make response data success case
# #         resData['status'] = 'success'
# #         resData['data'] = token
# #         resData['message'] = ApiResponseMessage.userCreatedSuccess.value
# #         resData['errors'] = []
# #         status_code = 201
# #     else:
# #         # Make response data fail case
# #         res = setException(serializer)
# #         resData['status'] = 'error'
# #         resData['data'] = {}
# #         resData['message'] = res.get('message')
# #         resData['errors'] = res.get('errors')
# #         status_code = 200
# #     return Response(resData, status=status_code)
#
#
# @swagger_auto_schema(
#     method='post',
#     request_body=CreatePatientUserSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# def register(request):
#     resData = dict()
#     # Initialize user serializer to validate data
#     serializer = CreatePatientUserSerializer(data=request.data)
#     if serializer.is_valid():
#         userData = {
#             'mobile_number': serializer.data.get('mobile_number'),
#             'email': serializer.data.get('email'),
#         }
#         UserQuery.createPatientUser(userData)
#         email = serializer.data.get('email')
#         mobile_number = serializer.data.get('mobile_number')
#         # If user registered with Email
#         if email != '' and email is not None:
#             user = UserQuery.getUserByEmail(email)
#             patient = PatientsDetail()
#             patient.pateint_id = user
#             # Create password forgot url and save in db
#             service = MainService(request)
#             user = service.forgotPasswordOtp(user)
#             # Send email to user#
#             EmailService(request, user, EmailType.signupOtp.value)
#             # Get Access Token
#             token = MainService.getJwtToken('ACCESS_TOKEN', user)
#             # Make response data success case#
#             resData['status'] = 'success'
#             resData['data'] = token
#             resData['message'] = ApiResponseMessage.emailSent.value
#             resData['errors'] = []
#             status_code = 200
#         # if user registered with Mobile Number
#         else:
#             user = UserQuery.getUserByMobileNumber(mobile_number)
#             patient = PatientsDetail()
#             patient.pateint_id = user
#             resData['status'] = 'success'
#             resData['data'] = {}
#             resData['message'] = ApiResponseMessage.emailSent.value
#             resData['errors'] = []
#             status_code = 200
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
#     request_body=LoginUserSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# def login(request):
#     resData = dict()
#     # Initialize user serializer to validate data
#     serializer = LoginUserSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.data['email']
#         user = UserQuery.getUserByEmail(email)
#         # Get Access Token
#         token = MainService.getJwtToken('ACCESS_TOKEN', user)
#         # Make response data success case
#         resData['status'] = 'success'
#         resData['data'] = token
#         resData['message'] = LoginMessages.you_are_now_logged_in.value
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
#
#
# @swagger_auto_schema(
#     method='get',
#     responses=responseData
# )
# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def userProfile(request):
#     resData = dict()
#     user = UserQuery.getUserById(request.user.id)
#     serializer = UserProfileSerializer(instance=user)
#     # Make response data success case
#     resData['status'] = 'SUCCESS'
#     resData['data'] = serializer.data
#     resData['message'] = ApiResponseMessage.dataSentSuccess.value
#     resData['errors'] = []
#     status_code = 200
#     return Response(resData, status=status_code)
#
#
# @swagger_auto_schema(
#     method='put',
#     request_body=EditProfileSerializer,
#     responses=responseData
# )
# @api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def editProfile(request, id):
#     resData = dict()
#     user = UserQuery.getUserById(id)
#     serializer = EditProfileSerializer(data=request.data, instance=user, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         # Make response data success case
#         resData['status'] = 'success'
#         resData['data'] = serializer.data
#         resData['message'] = ApiResponseMessage.userEditProfile.value
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
#     request_body=EditProfileImageSerializer,
#     responses=responseData
# )
# @api_view(['POST'])
# @parser_classes([FormParser, MultiPartParser])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def updateProfileImage(request):
#     resData = dict()
#     user = UserQuery.getUserById(request.user.id)
#     serializer = EditProfileImageSerializer(data=request.data, instance=user, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         # Make response data success case
#         resData['status'] = 'success'
#         resData['data'] = serializer.data
#         resData['message'] = ApiResponseMessage.userEditProfileImage.value
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
