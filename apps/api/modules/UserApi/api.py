from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from DjangoBaseSetup.common_modules.mainService import Status, MainService
from apps.api.modules import setException, responseData
from apps.api.ApiMessages import CommonApiMessages, UserApiMessages
from apps.api.modules.UserApi.serializer import RegisterUserSerializer, LoginUserSerializer, UserSerializer, \
    UpdateUserSerializer
from apps.api.modules.UserApi.service import UserQueryService


@swagger_auto_schema(
    method='post',
    request_body=RegisterUserSerializer,
    responses=responseData
)
@api_view(['POST'])
def register(request):
    resData = dict()
    # Initialize register UserApi serializer to validate data
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = None
        resData['message'] = UserApiMessages.user_register_successfully.value
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
    request_body=LoginUserSerializer,
    responses=responseData
)
@api_view(['POST'])
def login(request):
    resData = dict()
    # Initialize register UserApi serializer to validate data
    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid():
        userObj = UserQueryService.getUserByEmail(serializer.data.get('email', None))
        userSerializer = UserSerializer(instance=userObj)
        token = MainService.getJwtToken('ACCESS_TOKEN', userObj)
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = {'token': token, 'user': userSerializer.data}
        resData['message'] = UserApiMessages.login_successfully.value
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
    request_body=UserSerializer,
    responses=responseData
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user(request):
    userObj = UserQueryService.getUserById(request.user.id)
    userSerializer = UserSerializer(instance=userObj)
    resData = dict()
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {'user': userSerializer.data}
    resData['message'] = CommonApiMessages.data_sent_successfully.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='post',
    request_body=UpdateUserSerializer,
    responses=responseData
)
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateUser(request):
    resData = dict()
    userObj = UserQueryService.getUserById(request.user.id)
    serializer = UpdateUserSerializer(data=request.data, instance=userObj, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        userObj = UserQueryService.getUserById(request.user.id)
        updateUserSerializer = UpdateUserSerializer(instance=userObj)
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = {'user': updateUserSerializer.data}
        resData['message'] = UserApiMessages.user_updated_successfully.value
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
