from django.urls import path
from .views import LoginView, LogoutView, token_issue

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', token_issue, name='token_issue'),
]
