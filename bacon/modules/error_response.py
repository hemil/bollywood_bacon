from django.http import HttpResponse
import json
from django.conf import settings


def get_http_response(status_code, message):
    response_json = json.dumps({
        'status': 1,
        'data': message,
        'instance_name': settings.INSTANCE_NAME,
        'count': 0
    })
    return HttpResponse(response_json, content_type="application/json", status=status_code)
