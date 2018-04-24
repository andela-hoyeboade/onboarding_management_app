from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()
signup_url = reverse('api_signup')


class UserSignUpAPIIntegrationTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signup_data = dict(username='test_user',password='password',
                               email='test_user@gmail.com')

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
    def test_user_get_validation_error_if_required_fields_are_missing(self, user_field):
        data = self.signup_data.copy()
        data.pop(user_field)
        response = self.client.post(signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data[user_field])

    def test_user_get_token_after_signup(self):
        response = self.client.post(signup_url, self.signup_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['token'])

    @parameterized.expand([
        'username',
        'email',
    ])
    def test_user_cannot_signup_with_existing_username_or_email(self, user_field):
        User.objects.create(**self.signup_data)

        new_user_data = dict(username='test_user2',
                             email='test_user2@gmail.com',
                             password='password')
        new_user_data[user_field] = self.signup_data[user_field]

        response = self.client.post(signup_url, new_user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data[user_field])

    def test_user_cannot_signup_with_username_more_than_150_characters(self):
        user_data = self.signup_data.copy()
        user_data['username'] = 'username' * 20

        response = self.client.post(signup_url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['username'])
