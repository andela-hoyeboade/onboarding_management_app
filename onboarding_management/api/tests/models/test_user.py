from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_string_representation_of_user_model(self):
        user = User.objects.create(username='test_user')
        self.assertEqual(str(user), '<User username=test_user>')
