from django.conf.urls import url

from .views.users import signup

urlpatterns = [
    url(r'auth/signup', signup.SignUpAPIView.as_view(), name='api_signup')
]
