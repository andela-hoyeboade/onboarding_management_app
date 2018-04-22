from rest_framework_jwt.settings import api_settings

from ..models import User


class UserService(object):

    @staticmethod
    def create_user(user_data):
        username = user_data['username']
        password = user_data['password']
        email = user_data['email']

        return User.objects.create_user(username=username, password=password, email=email)

    @staticmethod
    def generate_user_token(user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)
