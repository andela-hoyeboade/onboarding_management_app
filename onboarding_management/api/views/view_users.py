from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSignUpSerializer
from ..create_user import create_user
from ..utils import generate_user_token


User = get_user_model()


class SignUpAPIView(APIView):

    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(serializer.validated_data)
        token = generate_user_token(user)

        return Response({'token': token}, status.HTTP_201_CREATED)

