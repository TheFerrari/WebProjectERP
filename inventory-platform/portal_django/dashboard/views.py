import logging
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def health(_request):
    return JsonResponse({'status': 'ok', 'service': 'portal_django'})


def _call_fastapi(path: str, token: str):
    headers = {'Authorization': f'Bearer {token}', 'X-Request-ID': 'portal-dashboard'}
    timeout = 2
    for _ in range(2):
        try:
            resp = requests.get(f"{settings.FASTAPI_INTERNAL_URL}{path}", headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.json(), None
        except requests.RequestException as exc:
            logger.warning('FastAPI call failed: %s', exc)
            timeout += 1
    return None, 'Service temporarily unavailable.'


@login_required
def dashboard(request):
    token_resp = requests.get(
        request.build_absolute_uri('/accounts/api/token/'),
        cookies=request.COOKIES,
        headers={'X-Requested-With': 'internal-dashboard-token'},
        timeout=2,
    )
    token = token_resp.json().get('access_token') if token_resp.ok else None

    context = {'inventory': [], 'orders': [], 'error': None}
    if token:
        inv, err1 = _call_fastapi('/v1/stock/summary', token)
        ords, err2 = _call_fastapi('/v1/orders/recent', token)
        context['inventory'] = inv or []
        context['orders'] = ords or []
        context['error'] = err1 or err2
    else:
        context['error'] = 'Unable to obtain auth token.'

    return render(request, 'dashboard/index.html', context)
