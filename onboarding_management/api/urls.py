from django.conf.urls import url

from .views.users import signup, login

urlpatterns = [
    url(r'auth/signup/$', signup.SignUpAPIView.as_view(), name='api_signup'),
    url(r'auth/login/$', login.LogInAPIView.as_view(), name='api_login'),
]
