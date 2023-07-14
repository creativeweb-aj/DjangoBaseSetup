from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.modules import responseData
from DjangoBaseSetup.common_modules.mainService import Status
from apps.api.ApiMessages import CommonApiMessages
from apps.api.modules.CmsApi.service import CmsService


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
def privacyPolicy(request):
    privacyPolicyData = CmsService.getCmsData('Privacy-Policy')
    resData = dict()
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {"privacy_policy": privacyPolicyData}
    resData['message'] = CommonApiMessages.data_sent_successfully.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
def termsConditions(request):
    privacyPolicyData = CmsService.getCmsData('Term-&-Conditions')
    resData = dict()
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {"terms_condition": privacyPolicyData}
    resData['message'] = CommonApiMessages.data_sent_successfully.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)


@swagger_auto_schema(
    method='get',
    responses=responseData
)
@api_view(['GET'])
def about(request):
    privacyPolicyData = CmsService.getCmsData('About')
    resData = dict()
    # Make response data success case
    resData['status'] = Status.success.value
    resData['data'] = {"about": privacyPolicyData}
    resData['message'] = CommonApiMessages.data_sent_successfully.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)
