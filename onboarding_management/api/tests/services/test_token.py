from unittest.mock import patch

from django.test import TestCase

from api.models import User
from api.services import token_service


class TokenServiceTest(TestCase):

    def setUp(self):
        self.user_data = {'username': 'test_user', 'password': 'test_password', 'email': 'test_email@gmail.com'}

    @patch('api.services.token.api_settings.JWT_ENCODE_HANDLER')
    @patch('api.services.token.api_settings.JWT_PAYLOAD_HANDLER')
    def test_generate_user_token(self, jwt_payload_handler_mock, jwt_encode_handler_mock):
        user = User(**self.user_data)
        user_jwt_payload = {}
        expected_token = 'test_token'

        jwt_payload_handler_mock.return_value = user_jwt_payload
        jwt_encode_handler_mock.return_value = expected_token

        generated_token = token_service.generate_user_token(user)

        jwt_payload_handler_mock.assert_called_with(user)
        jwt_encode_handler_mock.assert_called_with(user_jwt_payload)

        self.assertEqual(generated_token, expected_token)


class TokenServiceIntegrationTest(TestCase):

    pass