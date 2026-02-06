from django.contrib import admin
from django.urls import path, include
from core.views import health_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('health', health_view, name='health'),
]
