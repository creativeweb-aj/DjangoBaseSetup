from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from DjangoBaseSetup.common_modules.mainService import Status, MainService
from DjangoBaseSetup.messages.messages import UserApiMessages
from apps.api.modules import setException, responseData
from apps.api.modules.UserApi.serializer import RegisterUserSerializer, LoginUserSerializer, UserSerializer
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
    request_body=LoginUserSerializer,
    responses=responseData
)
@api_view(['POST'])
def login(request):
    resData = dict()
    # Initialize register UserApi serializer to validate data
    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid():
        user = UserQueryService.getUserByEmail(serializer.data.get('email', None))
        userSerializer = UserSerializer(instance=user)
        token = MainService.getJwtToken('ACCESS_TOKEN', user)
        # Make response data success case
        resData['status'] = Status.success.value
        resData['data'] = {'token': token, 'UserApi': userSerializer.data}
        resData['message'] = UserApiMessages.login_successfully.value
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
