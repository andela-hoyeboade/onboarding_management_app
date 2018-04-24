from unittest.mock import patch
from django.test import TestCase

from parameterized import parameterized

from api.models import User
from api.services import user_service


class UserServiceTest(TestCase):

    def setUp(self):
        self.user_data = {'username': 'test_user', 'password': 'test_password', 'email': 'test_email@gmail.com'}

    @patch('api.services.user.User.objects.create_user')
    def test_create_user_with_user_data(self, user_create_mock):
        expected_user = User(**self.user_data)
        user_create_mock.return_value = expected_user

        created_user = user_service.create_user(self.user_data)

        user_create_mock.assert_called_with(username=self.user_data['username'],
                                            password=self.user_data['password'],
                                            email=self.user_data['email'])
        self.assertEqual(created_user, expected_user)

    @parameterized.expand([
        'username',
        'email'
    ])
    @patch('api.services.user.User.objects.get')
    def test_get_user_by_username_or_email(self, user_field, user_get_mock):
        expected_user = User(**self.user_data)
        user_get_mock.return_value = expected_user

        user = user_service.get_user(self.user_data[user_field])
        self.assertEqual(user, expected_user)


class UserServiceIntegrationTest(TestCase):

    def setUp(self):
        self.user_data = {'username': 'test_user', 'password': 'test_password', 'email': 'test_email@gmail.com'}

    def test_create_user(self):
        User.objects.create_user(**self.user_data)

        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_get_user_with_existing_username_or_email(self):
        expected_user = User.objects.create_user(**self.user_data)

        self.assertEqual(user_service.get_user(self.user_data['username']), expected_user)
        self.assertEqual(user_service.get_user(self.user_data['email']), expected_user)

    def test_get_user_with_non_existing_username_or_email_raises_object_does_not_exist(self):

        with self.assertRaises(User.DoesNotExist):
            user_service.get_user('invalid')
