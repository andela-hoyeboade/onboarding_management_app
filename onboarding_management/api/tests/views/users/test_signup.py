import copy

from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()
signup_url = reverse('api_signup')


class UserSignUpAPIIntegrationTest(APITestCase):

    def setUp(self):
        self.signup_data = {'username': 'test_user',
                            'password': 'password',
                            'email': 'test_user@gmail.com'}

    def test_user_can_signup(self):
        response = self.client.post(signup_url, self.signup_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username=self.signup_data['username']).exists())
        self.assertTrue(User.objects.filter(email=self.signup_data['email']).exists())

    @parameterized.expand([
        'username',
        'password'
    ])
    def test_user_get_validation_error_if_required_fields_are_missing(self, field):
        data = copy.deepcopy(self.signup_data)
        data.pop(field)
        response = self.client.post(signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(field in response.data)

    def test_user_get_token_after_signup(self):
        response = self.client.post(signup_url, self.signup_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue(response.data['token'])
