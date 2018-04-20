from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


User = get_user_model()
signup_url = reverse('api_signup')


class UserSignUpAPITest(APITestCase):

    def setUp(self):
        self.signup_data = {'username': 'hassan', 'password': 'hassan', 'email': 'hassan@gmail.com'}

    def test_user_can_signup(self):
        response = self.client.post(signup_url, self.signup_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(username=self.signup_data['username']).exists())
