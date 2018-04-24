from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy

User = get_user_model()
login_url = reverse_lazy('api_login')


class UserLogInAPIIntegrationTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signup_data = {'username': 'test_user',
                           'password': 'password',
                           'email': 'test_user@gmail.com'}
        User.objects.create_user(**cls.signup_data)

    def test_user_can_login_with_username(self):
        user_data = self.signup_data.copy()
        user_data.pop('email')

        response = self.client.post(login_url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])

    def test_user_can_login_with_email_as_username(self):
        user_data = self.signup_data.copy()
        user_data['username'] = user_data['email']
        user_data.pop('email')

        response = self.client.post(login_url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])

    @parameterized.expand([
        'username',
        'password',
    ])
    def test_user_get_400_response_when_logging_without_required_fields(self, user_field):
        user_data = self.signup_data.copy()
        user_data.pop(user_field)

        response = self.client.post(login_url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data[user_field])

    def test_user_get_401_response_and_no_token_when_logging_with_invalid_password(self):
        user_data = self.signup_data.copy()
        user_data['password'] = 'incorrect'

        response = self.client.post(login_url, user_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('token' in response.data)
        self.assertEqual(response.data['detail'], 'Incorrect username or password')
