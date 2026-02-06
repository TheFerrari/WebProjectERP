from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'


class LogoutView(DjangoLogoutView):
    pass


@login_required
def token_issue(request):
    user = request.user
    groups = list(user.groups.values_list('name', flat=True))
    payload = {
        'sub': str(user.id),
        'username': user.username,
        'roles': groups,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXP_MINUTES),
        'iss': 'portal_django',
    }
    token = jwt.encode(payload, settings.DJANGO_JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return JsonResponse({'access_token': token, 'token_type': 'bearer'})
