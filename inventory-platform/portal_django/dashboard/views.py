import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def _request_with_retry(path, token):
    headers = {'Authorization': f'Bearer {token}'}
    last_error = None
    for _ in range(settings.PORTAL_REQUEST_RETRIES + 1):
        try:
            response = requests.get(
                f"{settings.FASTAPI_BASE_URL}{path}",
                headers=headers,
                timeout=settings.PORTAL_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            return response.json(), None
        except Exception as exc:
            last_error = str(exc)
    return None, last_error

@login_required
def dashboard_view(request):
    token_resp = requests.get(
        request.build_absolute_uri('/accounts/api/token'),
        cookies=request.COOKIES,
        timeout=settings.PORTAL_REQUEST_TIMEOUT,
    )
    token = token_resp.json().get('access_token') if token_resp.ok else None

    context = {'inventory': [], 'orders': [], 'error': None}
    if token:
        inventory, inv_error = _request_with_retry('/v1/stock/summary', token)
        orders, ord_error = _request_with_retry('/v1/orders/recent', token)
        context['inventory'] = inventory or []
        context['orders'] = orders or []
        context['error'] = inv_error or ord_error
    else:
        context['error'] = 'Unable to obtain API token'
    return render(request, 'dashboard/home.html', context)
