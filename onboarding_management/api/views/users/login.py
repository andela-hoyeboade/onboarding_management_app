from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...serializers.users.login import UserLogInSerializer
from ...services import token_service, user_service


User = get_user_model()


class LogInAPIView(APIView):
    """
    View to handle user login
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = UserLogInSerializer

    def post(self, request):
        """
        Validate user and returns generated token for user
        :return: Response
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_service.get_user(serializer.validated_data['username'])

            if user.check_password(serializer.validated_data['password']):
                token = token_service.generate_user_token(user)
                return Response({'token': token}, status.HTTP_200_OK)

            return Response({'detail': 'Incorrect username or password'},
                            status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({'detail': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
