from django.contrib import admin
from django.urls import include, path
from dashboard.views import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('health/', health, name='health'),
]
