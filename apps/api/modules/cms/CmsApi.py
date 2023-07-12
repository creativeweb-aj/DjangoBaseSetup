from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.modules import responseData
from zeero_bills.common_modules.mainService import Status
from zeero_bills.messages.messages import ApiResponseMessage
from apps.api.modules.cms.CmsService import CmsService


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
    resData['message'] = ApiResponseMessage.dataSentSuccess.value
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
    resData['message'] = ApiResponseMessage.dataSentSuccess.value
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
    resData['message'] = ApiResponseMessage.dataSentSuccess.value
    resData['errors'] = []
    status_code = 200
    return Response(resData, status=status_code)
