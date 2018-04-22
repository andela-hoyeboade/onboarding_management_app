import unittest
from unittest.mock import patch

from api.models import User
from api.services.user import UserService


class UserServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_service = UserService

    def setUp(self):
        self.user_data = {'username': 'test_user', 'password': 'test_password', 'email': 'test_email@gmail.com'}

    @patch('api.services.user.User.objects.create_user')
    def test_create_user_with_user_data(self, mock_user_create):
        expected_user = User(**self.user_data)
        mock_user_create.return_value = expected_user

        created_user = self.user_service.create_user(self.user_data)

        mock_user_create.assert_called_with(username=self.user_data['username'],
                                            password=self.user_data['password'],
                                            email=self.user_data['email'])
        self.assertEqual(created_user, expected_user)

    @patch('api.services.user.api_settings.JWT_ENCODE_HANDLER')
    @patch('api.services.user.api_settings.JWT_PAYLOAD_HANDLER')
    def test_generate_user_token(self, jwt_payload_handler_mock, jwt_encode_handler_mock):
        user = User(**self.user_data)
        user_jwt_payload = {}
        expected_token = 'test_token'

        jwt_payload_handler_mock.return_value = user_jwt_payload
        jwt_encode_handler_mock.return_value = expected_token

        generated_token = self.user_service.generate_user_token(user)

        jwt_payload_handler_mock.assert_called_with(user)
        jwt_encode_handler_mock.assert_called_with(user_jwt_payload)

        self.assertEqual(generated_token, expected_token)



