from .models import User


def create_user(user_data):
    username = user_data['username']
    password = user_data['password']
    email = user_data.get('email')

    return User.objects.create_user(username=username, password=password, email=email)
