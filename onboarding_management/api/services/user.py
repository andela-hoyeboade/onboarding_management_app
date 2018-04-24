from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class UserService:

    @staticmethod
    def create_user(user_data):
        """
        :param user_data: a dictionary of user data
        :return: created user object
        """

        return User.objects.create_user(**user_data)

    @staticmethod
    def get_user(username_or_email):
        """
        :param username_or_email: the username or email for a user
        :return: user object
        :raise: User.DoesNotExist
        """
        return User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
