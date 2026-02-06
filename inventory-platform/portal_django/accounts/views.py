from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def token_view(request):
    groups = [g.name for g in request.user.groups.all()]
    payload = {
        'sub': str(request.user.id),
        'username': request.user.username,
        'roles': groups,
        'exp': datetime.now(timezone.utc) + timedelta(hours=2),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return JsonResponse({'access_token': token, 'token_type': 'bearer'})
