from drf_yasg import openapi

# Response Body Default Schema
pageParam = openapi.Parameter(
    'page',
    openapi.IN_QUERY,
    description="Send page number in query param",
    type=openapi.TYPE_STRING
)
responseData = {
    200: openapi.Schema(
        type=openapi.TYPE_STRING,
        status="SUCCESS",
        data=openapi.TYPE_OBJECT,
        message=openapi.TYPE_STRING
    ),
    400: openapi.Schema(
        type=openapi.TYPE_STRING,
        status="FAIL",
        data=openapi.TYPE_OBJECT,
        message=openapi.TYPE_STRING
    )
}


# Set error messages from serializer
def setException(serializer):
    errors = []
    message = ''
    for error in serializer.errors:
        if error == "non_field_errors":
            data = serializer.errors[error][0]
            errors.append(data)
            message = addString(message, serializer.errors[error][0])
        else:
            data = {
                "field": error,
                "message": serializer.errors[error][0]
            }
            errors.append(data)
            message = addString(message, serializer.errors[error][0])

    res = {
        "errors": errors,
        "message": message
    }
    return res


def addString(string, value):
    if string:
        if type(value) == dict:
            string = string + ', ' + value.get('message')
        else:
            string = string + ', ' + value
    else:
        if type(value) == dict:
            string = value.get('message')
        else:
            string = value
    return string
