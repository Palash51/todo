import logging
import traceback

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def sg_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try:
        data = response.data
        message = ""
        for key, value in data.items():
            message += "%s: %s. " % (key, value)
    except:
        message = ""

    if response is not None:
        response.data['statusCode'] = response.status_code
        response.data['status'] = 0
        response.data = {
            'status': 0,
            'message': message,
            'statusCode': response.status_code,
            'data': {}
        }
    return response


def api_response(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if res['status'] == 1:
                return Response({
                    'data': res.get('data', {}), 
                    'status': res.get('status', 1),
                    'statusCode': res.get('statusCode', 200),
                    'message': res.get('message', 'success'),
                    'exception': '',
                }, status=res.get('statusCode', 200))
            else:
                return Response({
                    'data': res.get('data', {}), 
                    'status': res.get('data', 0),
                    'statusCode': res.get('statusCode', 400),
                    'message': res.get('message', ''),
                    'exception': '',
                }, status=res.get('statusCode', 400))
        except Exception as e:
            logger.error(e)
            return Response({
                'data': {}, 
                'status': 0,
                'statusCode': 400,
                'message': "Something wrong. Please try again after sometime.",
                'exception': traceback.format_exc(),
            }, status=400)
    return wrapper
