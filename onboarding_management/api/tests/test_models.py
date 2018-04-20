from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTest(TestCase):

    def test_string_reprensentation_of_user_model(self):
        user = User.objects.create(username='hassan')
        self.assertEqual(str(user), '<User username=hassan>')
