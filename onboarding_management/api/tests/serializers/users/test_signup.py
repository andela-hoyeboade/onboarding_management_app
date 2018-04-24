from django.test import TestCase
from parameterized import parameterized
from rest_framework.exceptions import ValidationError

from api.serializers.users.signup import UserSignUpSerializer


class UserSignUpSerializerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = dict(username='test_user', email='test_user_@gmail.com', password='password')
        cls.serializer_class = UserSignUpSerializer

    def test_signup_serializer_is_valid_returns_true_for_valid_data(self):
        serializer = self.serializer_class(data=self.user_data)

        self.assertTrue(serializer.is_valid())

    @parameterized.expand((
        'username',
        'email',
        'password',
    ))
    def test_signup_serializer_contains_correct_data_after_validation(self, user_field):
        serializer = self.serializer_class(data=self.user_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data[user_field], self.user_data[user_field])

    @parameterized.expand((
            'username',
            'email',
            'password',
    ))
    def test_signup_serializer_contains_errors_for_missing_required_data(self, user_field):
        user_data = self.user_data.copy()
        user_data.pop(user_field)

        serializer = self.serializer_class(data=user_data)

        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors[user_field])

    def test_signup_serializer_contains_errors_for_invalid_email(self):
        user_data = self.user_data.copy()
        user_data['email'] = 'invalid_email'

        serializer = self.serializer_class(data=user_data)

        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors['email'])

    def test_signup_serializer_contains_errors_for_username_more_than_150(self):
        user_data = self.user_data.copy()
        user_data['username'] = 'username' * 150

        serializer = self.serializer_class(data=user_data)

        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors['username'])

    @parameterized.expand((
        'username',
        'email',
        'password',
    ))
    def test_signup_serializer_raises_errors_when_required_fields_are_missing_and_raise_exception_is_true(self,
                                                                                                          user_field):
        user_data = self.user_data.copy()
        user_data.pop(user_field)

        serializer = self.serializer_class(data=user_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

