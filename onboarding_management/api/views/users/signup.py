from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...serializers.users.signup import UserSignUpSerializer
from ...services import user_service, token_service


User = get_user_model()


class SignUpAPIView(APIView):

    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_service.create_user(serializer.validated_data)
        token = token_service.generate_user_token(user)

        return Response({'token': token}, status.HTTP_201_CREATED)
