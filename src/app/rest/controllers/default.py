from app.rest.models import AccountModel, RequestModel
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from app.rest.utils import AXESS
from ipware import get_client_ip
import json


@csrf_exempt
def handler(request, method):
    try:
        access_token = request.headers['Authorization']
    except:
        return JsonResponse({
            'message': 'ERROR: Access token not found in request headers.',
        })

    try:
        account = AccountModel.objects.get(
            pk=access_token,
            active=True,
        )
    except:
        return JsonResponse({
            'message': 'ERROR: You do not have permission to make request.',
        })

    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({
            'message': 'ERROR: Request body must be in application/json format',
        })

    try:
        session, payload, response = AXESS(account).execute(method, payload)
    except:
        return JsonResponse({
            'message': 'ERROR: An error occurred while processing the request.',
        })

    ip_address, _ = get_client_ip(request)

    RequestModel.objects.create(
        response=response.json(),
        ip_address=ip_address,
        session=session,
        payload=payload,
        method=method,
    )

    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )
