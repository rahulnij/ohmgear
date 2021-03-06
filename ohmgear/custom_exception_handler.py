from rest_framework.views import exception_handler
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status'] = False
        if 'detail' in response.data:
            response.data['data'] = response.data['detail']
        #response.data['data'] = ''
        response.data['detail'] = ''

    return response


def custom404(request):
    return JsonResponse({
        'status': False,
        'data': 'The resource was not found'
    })
