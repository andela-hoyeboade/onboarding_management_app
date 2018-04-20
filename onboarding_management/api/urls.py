from django.urls import path

from .views import view_users

urlpatterns = [
    path('auth/signup', view_users.SignUpAPIView.as_view(), name='api_signup')
]
